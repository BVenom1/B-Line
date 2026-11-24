from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
from database import get_db
from models import (User, UserModel, SessionToken)
from security import hash_password, verify_password
from routes import sessions

router = APIRouter(prefix="/user", tags=["user"])

# POST /signup
class SignupModel(BaseModel):
    user_name: str
    email: str
    password: str
    status: str | None

@router.post("/signup")
async def signup(user: SignupModel, db: AsyncSession = Depends(get_db)) -> UserModel:
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

    # TODO: password strength check
    
    db_user = User(
        user_name = user.user_name,
        email = user.email,
        password_hash = hash_password(user.password),
        status = user.status
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # TODO: send verification email

    return db_user.clean_return()

# POST /login
class LoginModel(BaseModel):
    uname_or_email: str
    password: str

class LoginResponse(BaseModel):
    user: UserModel
    token: str

@router.post("/login")
async def login(login: LoginModel, db: AsyncSession = Depends(get_db)) -> LoginResponse:
    check = await db.scalar(select(User).where(or_(
        User.email == login.uname_or_email,
        User.user_name == login.uname_or_email
    )))
    if check == None or not verify_password(login.password, check.password_hash):
        raise HTTPException(401, "Incorrect username/email or password")

    await db.execute(delete(SessionToken).where(
        SessionToken.user_id == check.user_id
    ))

    await sessions.remove_sessions(check.user_id, db)
    token = await sessions.add_session(check.user_id, db)

    return LoginResponse(user=check.clean_return(), token=token)