'''
This is the file where the FastAPI app and endpoints are defined.
'''
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from database import get_db, init_models

from models import (
    User, UserModel,
    Group, GroupModel,
    Membership, MembershipModel, MembershipTypes
)

# create API application
app = FastAPI(lifespan=init_models)

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

    user.user_id = None
    user.created_at = None      # reset creation & verification dates to prevent user from
    user.verified_at = None     # accessing messages from before their account was created
    # TODO: password strength check
    # TODO: password hashing
    
    db_user = User.from_schema(user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: send verification email

    return user.clean_return()

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

    return UserModel.model_validate(check).clean_return()

# POST /create-group
class CreateGroupModel(BaseModel):
    user: UserModel         # TODO: check if user is logged in (using web tokens or something else)
    group: GroupModel

@app.post("/create-group")
async def create_group(group_info: CreateGroupModel, db: AsyncSession = Depends(get_db)) -> GroupModel:
    # check if user exists. TODO: check if user is logged in using a session token
    check = await db.scalar(select(User).where(User.user_id == group_info.user.user_id))
    if check == None: raise HTTPException(401, "Given user does not exist")

    # create database entry of group, add to groups table
    group_info.group.created_at = None                      # reset group creation date
    group_info.group.group_id = None
    db_group = Group.from_scema(group_info.group)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)

    # create database entry of given user as an admin of the group, add to memberships table
    membership = MembershipModel(
        user_id = group_info.user.user_id,
        group_id = db_group.group_id,
        membership_type = MembershipTypes.ADMIN
    )
    db_membership = Membership.from_schema(membership)
    db.add(db_membership)
    await db.commit()
    await db.refresh(db_membership)

    return GroupModel.model_validate(db_group)