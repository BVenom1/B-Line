'''
This is the file where the FastAPI app and endpoints are defined.
'''
from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from database import get_db

from models import (
    User, UserModel
)

# create API application
app = FastAPI()

# create API endpoints
@app.get("/test")
async def test():
    return "this is a test"

@app.post("/signup")
async def signup(user: UserModel, db: AsyncSession = Depends(get_db)):
    check = await db.scalar(select(User).where(or_(
        User.email == user.email,
        User.user_name == user.user_name
    )))
    if check != None:
        if check.email.lower() == user.email.lower():
            raise HTTPException(400, "Given email is already in use. Try logging in")
        else:
            raise HTTPException(400, "Given username is taken. Try another username")

    # TODO: password strength check
    # TODO: password hashing
    
    db_user = User.from_schema(user)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: send verification email

    return user.clean_return()
