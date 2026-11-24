'''
This is the file where the FastAPI app and endpoints are defined.
'''
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from database import get_db, init_models

from models import (
    User, UserModel,
    Conversation,
    Group, GroupModel,
    Membership, MembershipModel, MembershipTypes,
    Contact, ContactModel,
)

# create API application
app = FastAPI(lifespan=init_models)

# add middleware to allow tauri app to communicate
origins = [
    "http://localhost:1420",
    "http://127.0.0.1:1420"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# create API endpoints
@app.get("/test")
async def test():
    return "this is a test"

# POST /signup
@app.post("/signup")
async def signup(user: UserModel, db: AsyncSession = Depends(get_db)) -> UserModel:
    check = await db.scalar(select(User).where(or_(
        User.email == user.email,
        User.user_name == user.user_name
    )))
    if check != None:
        if check.email.lower() == user.email.lower():
            raise HTTPException(409, "Given email is already in use. Try logging in")
        elif check.user_name == user.user_name:
            raise HTTPException(409, "Given username is taken. Try another username")
        else:
            raise HTTPException(409, "Something went wrong. Please try again")

    user.user_id = None         # reset user_id (prevents arbitrary user_id insertions)
    user.created_at = None      # reset creation & verification dates to prevent user from
    user.verified_at = None     # accessing messages from before their account was created
    # TODO: password strength check
    # TODO: password hashing
    
    db_user = User.from_schema(user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: send verification email

    return db_user.clean_return()

# POST /login
class LoginModel(BaseModel):
    uname_or_email: str
    password: str

@app.post("/login")
async def login(login: LoginModel, db: AsyncSession = Depends(get_db)) -> UserModel:
    print(login)
    #TODO: password hashing
    check = await db.scalar(select(User).where(or_(
        User.email == login.uname_or_email,
        User.user_name == login.uname_or_email
    )))
    if check == None or check.password != login.password:
        raise HTTPException(401, "Incorrect username/email or password")

    return check.clean_return()

# POST /user-{user_id}/create-group
@app.post("/user-{user_id}/create-group")
async def create_group(user_id: int, group: GroupModel, db: AsyncSession = Depends(get_db)) -> GroupModel:
    # check if user exists. TODO: check if user is logged in using a session token
    check = await db.scalar(select(User).where(User.user_id == user_id))
    if check == None: raise HTTPException(401, "Given user does not exist")

    # create conversation for the group
    db_conversation = Conversation()
    db.add(db_conversation)
    await db.commit()
    await db.refresh(db_conversation)

    # create database entry of group, add to groups table
    group.created_at = None     # reset group creation date
    group.group_id = None       # reset group_id (prevents arbitrary group_id insertions)
    group.conversation_id = db_conversation.conversation_id     # attach conversation to group
    db_group = Group.from_scema(group)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)

    # create database entry of given user as an admin of the group, add to memberships table
    membership = MembershipModel(
        user_id = user_id,
        group_id = db_group.group_id,
        membership_type = MembershipTypes.ADMIN
    )
    db_membership = Membership.from_schema(membership)
    db.add(db_membership)
    await db.commit()
    await db.refresh(db_membership)

    return db_group.clean_return()

# GET /user-{user_id}/group-{group_id}/get-group-members
class MembershipUserModel(BaseModel):
    membership: MembershipModel
    user: UserModel

@app.get("/user-{user_id}/group-{group_id}/get-group-members")
async def get_group_members(user_id: int, group_id: int, db: AsyncSession = Depends(get_db)) -> list[MembershipUserModel]:
    # TODO: check if user is valid and logged in
    check = await db.scalar(select(Membership).where(and_(
        Membership.user_id == user_id,
        Membership.group_id == group_id
    )))
    if check == None: raise HTTPException(404, "Group not found")

    db_members = (
        await db.execute(select(Membership, User)
        .join(User, Membership.user_id == User.user_id)
        .where(Membership.group_id == group_id))
    ).all()
    return [
        MembershipUserModel(membership=membership.clean_return(), user=user.clean_return())
        for membership, user in db_members
    ]

# PUT /user-{user_id}/group-{group_id}/add_friend-{friend_id}
@app.put("/user-{user_id}/group-{group_id}/add_friend-{friend_id}")
async def add_friend(user_id: int, group_id: int, friend_id: int, db: AsyncSession = Depends(get_db)) -> MembershipModel:
    # TODO: check if user is valid and logged in

    # check if the user is an admin in the group
    check = await db.scalar(select(Membership).where(and_(
        Membership.user_id == user_id,
        Membership.group_id == group_id
    )))
    if check == None: raise HTTPException(404, "Group not found")
    elif check.membership_type != MembershipTypes.ADMIN: raise HTTPException(403, "User does not have admin privilege")

    # check if the friend is a member in the group
    check = await db.scalar(select(Membership).where(and_(
        Membership.user_id == friend_id,
        Membership.group_id == group_id
    )))
    if check != None: raise HTTPException(409, "User's friend is already in the group")

    # add friend to group
    db_membership = Membership.from_schema(MembershipModel(
        user_id=friend_id,
        group_id=group_id
    ))
    db.add(db_membership)
    await db.commit()
    await db.refresh(db_membership)

    return db_membership.clean_return()

# GET /user-{user_id}/get_groups
@app.get("/user-{user_id}/get_groups")
async def get_groups(user_id: int, db: AsyncSession = Depends(get_db)) -> list[GroupModel]:
    # TODO: check if user exists & is logged in

    db_groups = await db.scalars(
        select(Group)
        .join(Membership, Group.group_id == Membership.group_id)
        .where(Membership.user_id == user_id)
    )

    return [GroupModel.model_validate(x) for x in db_groups]

# POST /user-{user_id}/add_contact-{contact_uname_or_email}

@app.post("/user-{user_id}/add_contact-{contact_uname_or_email}")
async def add_contact(user_id: int, contact_uname_or_email: str, db: AsyncSession = Depends(get_db)) -> ContactModel:
    check = await db.scalar(select(User).where(User.user_id == user_id))
    if check == None:
        raise HTTPException(401, "User does not exist")
    db_contact_user = await db.scalar(select(User).where(or_(
        User.email == contact_uname_or_email,
        User.user_name == contact_uname_or_email
    )))
    if db_contact_user == None:
        raise HTTPException(401, "Contact does not exist")

    db_conversation = Conversation()

    contact = ContactModel(
        user_id=user_id,
        contact_user_id=db_contact_user.user_id,
        conversation_id=db_conversation.conversation_id
    )

    db_contact = Contact.from_schema(contact)

    db.add(db_contact)
    await db.commit()
    await db.refresh(db_contact)

    return db_contact.clean_return()