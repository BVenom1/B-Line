'''
This is the file where the FastAPI app and endpoints are defined.
'''
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from database import get_db, init_models

from models import (
    User, UserModel
)

# create API application
app = FastAPI(lifespan=init_models)

# create API endpoints
@app.get("/test")
async def test():
    return "this is a test"

@app.post("/signup")
async def signup(user: UserModel, db: AsyncSession = Depends(get_db)) -> UserModel:
    check = await db.scalar(select(User).where(or_(
        User.email == user.email,
        User.user_name == user.user_name
    )))
    if check != None:
        if check.email.lower() == user.email.lower():
            raise HTTPException(409, "Given email is already in use. Try logging in")
        else:
            raise HTTPException(409, "Given username is taken. Try another username")

    # TODO: password strength check
    # TODO: password hashing
    
    db_user = User.from_schema(user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: send verification email

    return user.clean_return()

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
