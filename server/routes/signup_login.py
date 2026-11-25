from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, TypeAdapter, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, or_
from database import get_db, add_to_db
from models import (User, UserModel, SessionToken)
from routes import helpers

router = APIRouter(prefix="", tags=["user"])

# POST /signup
class SignupModel(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    status: str | None

def clean_username(user_name: str) -> str:
    clean_uname = user_name.strip()
    if clean_uname == "": raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail="Given username is empty"
    )
    try:
        TypeAdapter(EmailStr).validate_python(clean_uname)
    except ValidationError:
        return clean_uname
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail="Username cannot be an email address"
    )

@router.post("/signup")
async def signup(user: SignupModel, db: AsyncSession = Depends(get_db)) -> UserModel:
    clean_uname = clean_username(user.user_name)
    clean_email = user.email.strip().lower()

    check = await db.scalar(select(User).where(or_(
        User.email == clean_email,
        User.user_name == clean_uname
    )))
    if check != None:
        if check.email.lower() == clean_email:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Given email is already in use. Try logging in"
            )
        elif check.user_name == clean_uname:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Given username is taken. Try another username"
            )
        else:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "Something went wrong. Please try again"
            )

    # TODO: password strength 
    
    db_user = User(
        user_name = clean_uname,
        email = clean_email,
        password_hash = helpers.hash_password(user.password),
        status = (user.status or "").strip() or None
    )
    
    await add_to_db(
        db_user, db,
        lambda: HTTPException(
            status.HTTP_409_CONFLICT,
            "Conflict when registering user. please try again"
        ),
        commit=True
    )

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
    login.uname_or_email = login.uname_or_email.strip()
    if not login.uname_or_email: raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username/email or password"
    )

    check = await db.scalar(select(User).where(or_(
        User.email == login.uname_or_email.lower(),
        User.user_name == login.uname_or_email
    )))
    if check == None or not helpers.verify_password(login.password, check.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Incorrect username/email or password"
        )

    await helpers.remove_sessions(check.user_id, db)
    token = await helpers.add_session(check.user_id, db)
    await db.commit()

    return LoginResponse(user=check.clean_return(), token=token)

# @router.get("/test-{token}")
# async def test(token: str, db: AsyncSession = Depends(get_db)) -> UserModel:
#     user = await sessions.verify_session(token, db)
#     if user == None: 
#         raise HTTPException(404, "Error")
#     return user.clean_return()