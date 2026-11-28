from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends

from pwdlib import PasswordHash
import secrets, hashlib
from datetime import datetime, timezone

from models import (
    SessionToken, User,
    ContactStatus, Contact
)
from database import add_to_db, get_db

# Session Management Functions

def get_raw_token() -> str:
    return secrets.token_urlsafe(32)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()

async def remove_sessions(user_id: int, db: AsyncSession):
    await db.execute(
        delete(SessionToken).where(
            SessionToken.user_id == user_id
        )
    )
    await db.flush()

async def add_session(user_id: int, db: AsyncSession) -> str:
    token = get_raw_token()
    
    session = SessionToken(
        user_id = user_id,
        token_hash = hash_token(token)
    )
    await add_to_db(session, db, commit=False)
    return token


# Function for creating a dependency for Session Tokens

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    if credentials == None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authentication header",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_digest = hash_token(credentials.credentials)
    current_time = datetime.now(timezone.utc)

    db_user = (await db.execute(
        select(User)
        .join(SessionToken, SessionToken.user_id == User.user_id)
        .where(
            SessionToken.token_hash == token_digest,
            SessionToken.expires_at > current_time
        )
    )).scalar()

    if db_user == None: raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or Expired Session Token",
        headers={"WWW-Authenticate": "Bearer"}   
    )

    # TODO: add last_accessed_at field in SessionToken

    return db_user


# Functions for hashing & verifying passwords

hasher = PasswordHash.recommended()

def hash_password(raw_password: str) -> str:
    return hasher.hash(raw_password)

def verify_password(raw_password: str, password_hash: str) -> bool:
    return hasher.verify(raw_password, password_hash)


# function to get the contact addressed to a user

async def get_contact(
    db: AsyncSession,
    contact_id: int,
    user: User | None = None,
    contact_user: User | None = None,
    contact_status: ContactStatus | None = None,
) -> Contact:
    conditions = [Contact.contact_id == contact_id]
    if user: conditions.append(Contact.user_id == user.user_id)
    if contact_user: conditions.append(Contact.contact_user_id == contact_user.user_id)
    if status: conditions.append(Contact.contact_status == contact_status)
    
    db_contact = await db.scalar(select(Contact).where(*conditions))
    if db_contact is None: raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail="Contact not found"
    )
    return db_contact