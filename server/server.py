'''
This is the file where the FastAPI app and endpoints are defined.
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_models
from routes import signup_login, groups_memberships

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

app.include_router(signup_login.router, prefix="/api")
app.include_router(groups_memberships.router, prefix="/api")

# # PUT /user-{user_id}/group-{group_id}/add_friend-{friend_id}
# @app.put("/user-{user_id}/group-{group_id}/add_friend-{friend_id}")
# async def add_friend(user_id: int, group_id: int, friend_id: int, db: AsyncSession = Depends(get_db)) -> MembershipModel:
#     # TODO: check if user is valid and logged in

#     # check if the user is an admin in the group
#     check = await db.scalar(select(Membership).where(and_(
#         Membership.user_id == user_id,
#         Membership.group_id == group_id
#     )))
#     if check == None: raise HTTPException(404, "Group not found")
#     elif check.membership_type != MembershipTypes.ADMIN: raise HTTPException(403, "User does not have admin privilege")

#     # check if the friend is a member in the group
#     check = await db.scalar(select(Membership).where(and_(
#         Membership.user_id == friend_id,
#         Membership.group_id == group_id
#     )))
#     if check != None: raise HTTPException(409, "User's friend is already in the group")

#     # add friend to group
#     db_membership = Membership.from_schema(MembershipModel(
#         user_id=friend_id,
#         group_id=group_id
#     ))
#     db.add(db_membership)
#     await db.commit()
#     await db.refresh(db_membership)

#     return db_membership.clean_return()

# # POST /user-{user_id}/add_contact-{contact_uname_or_email}
# @app.post("/user-{user_id}/add_contact-{contact_uname_or_email}")
# async def add_contact(user_id: int, contact_uname_or_email: str, db: AsyncSession = Depends(get_db)) -> ContactModel:
#     check = await db.scalar(select(User).where(User.user_id == user_id))
#     if check == None:
#         raise HTTPException(401, "User does not exist")
#     db_contact_user = await db.scalar(select(User).where(or_(
#         User.email == contact_uname_or_email,
#         User.user_name == contact_uname_or_email
#     )))
#     if db_contact_user == None:
#         raise HTTPException(401, "Contact does not exist")

#     db_conversation = Conversation()
#     db.add(db_conversation)
#     await db.commit()
#     await db.refresh(db_conversation)

#     contact = ContactModel(
#         user_id=user_id,
#         contact_user_id=db_contact_user.user_id,
#         conversation_id=db_conversation.conversation_id
#     )

#     db_contact = Contact.from_schema(contact)

#     db.add(db_contact)
#     await db.commit()
#     await db.refresh(db_contact)

#     return db_contact.clean_return()

