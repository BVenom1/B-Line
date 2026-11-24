from sqlalchemy.ext.asyncio import AsyncSession
from models import (
    SessionToken
)
from sqlalchemy import delete, select
import secrets, hashlib

async def remove_sessions(user_id: int, db: AsyncSession):
    await db.execute(
        delete(SessionToken).where(
            SessionToken.user_id == user_id
        )
    )

async def add_session(user_id: int, db: AsyncSession) -> str:
    token = secrets.token_urlsafe(32)
    
    session = SessionToken(
        user_id = user_id,
        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return token

async def verify_session(token: str, db: AsyncSession) -> bool:
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    session = await db.scalar(select(SessionToken).where(
        SessionToken.token_hash == token_hash
    ))
    return session != None