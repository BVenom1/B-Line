'''
This is the file where the ORM models and pydantic scemas
related to the database tables are defined.
'''
from database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, false, DateTime
from sqlalchemy.dialects.postgresql import CITEXT

from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime

# users:
class UserModel(BaseModel):
    user_id: int | None = None
    user_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    status: str | None = None
    is_verified: bool = False
    created_at: datetime | None = None
    verified_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

    def clean_return(self) -> UserModel:
        return UserModel(
            user_id = self.user_id,
            user_name = self.user_name,
            email = self.email,
            status = self.status,
            is_verified = self.is_verified,
            created_at = self.created_at,
            verified_at = self.verified_at
        )

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[EmailStr] = mapped_column(CITEXT(255), unique=True)
    password: Mapped[str] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String)
    is_verified: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    @classmethod
    def from_schema(cls, user: UserModel) -> User:
        return User(
            user_id = user.user_id,
            user_name = user.user_name,
            email = user.email,
            password = user.password,
            status = user.status,
            is_verified = user.is_verified,
            created_at = user.created_at or datetime.now().astimezone(),
            verified_at = user.verified_at
        )