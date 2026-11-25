'''
This is the file where the database is set up.
'''
# Imports
import os, json

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from typing import AsyncGenerator, Callable

from fastapi import FastAPI

# Connect to the PostgreSQL database using credentials.json
credentials = {}
cred_file_loc = os.path.join(os.path.dirname(__file__), "credentials.json")
with open(cred_file_loc, "r", encoding="utf-8") as file:
    credentials = json.load(file)

# set up database
engine = create_async_engine(credentials["url"], echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False)
class Base(DeclarativeBase): pass

# function to generate session as a dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

# function to initialize all the tables in the database if they don't exist
async def init_models(_: FastAPI):
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS citext;"))
        await connection.run_sync(Base.metadata.create_all)
        yield

# function to add elements to database
class DatabaseError(Exception): pass

async def add_to_db(
    element: Base,
    db: AsyncSession,
    on_conflict: Callable[[], Exception] | None = None,
    commit: bool = False
) -> None:
    try:
        db.add(element)
        if commit: 
            await db.commit()
            await db.refresh(element)
        else:
            await db.flush()
    except IntegrityError as exc:
        await db.rollback()
        raise (
            on_conflict()
            if on_conflict is not None
            else DatabaseError("Database Error")
        ) from exc

# main function for testing
if __name__ == "__main__":
    print(credentials)