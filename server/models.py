'''
This is the file where the ORM models and pydantic scemas
related to the database tables are defined.
'''
from database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, false, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import CITEXT

from pydantic import BaseModel, EmailStr

from datetime import datetime, timezone, timedelta
import enum

SESSION_TTL_DAYS = 14       # the number of days for which the session token is valid

def date_func() -> datetime:
    return datetime.now(timezone.utc)

# users:
class UserModel(BaseModel):
    user_name: str
    email: EmailStr
    status: str | None = None
    is_verified: bool = False
    created_at: datetime
    verified_at: datetime | None = None

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(25), unique=True, index=True)
    email: Mapped[EmailStr] = mapped_column(CITEXT(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    status: Mapped[str | None] = mapped_column(String, default=None)
    is_verified: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func())
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    def clean_return(self) -> UserModel:
        return UserModel(
            user_name=self.user_name,
            email=self.email,
            status=self.status,
            is_verified=self.is_verified,
            created_at=self.created_at,
            verified_at=self.verified_at
        )

# session tokens:
class SessionToken(Base):
    __tablename__ = "session_tokens"
    session_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func())
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func() + timedelta(days=SESSION_TTL_DAYS))

# conversations:
class Conversation(Base):
    __tablename__ = "conversations"
    conversation_id: Mapped[int] = mapped_column(primary_key=True)

# groups:
class GroupModel(BaseModel):
    group_id: int
    group_name: str
    description: str | None = None
    created_at: datetime

class Group(Base):
    __tablename__ = "groups"
    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func())
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.conversation_id", ondelete="CASCADE"), nullable=False)

    def clean_return(self) -> GroupModel:
        return GroupModel(
            group_id=self.group_id,
            group_name=self.group_name,
            description=self.description,
            created_at=self.created_at,
        )

# memberships:
class MembershipTypes(enum.Enum):
    MEMBER = "member"
    ADMIN = "admin"
    BANNED = "banned"
    LEFT = "left"

class NotificationTypes(enum.Enum):
    NOTIFY = "notify"
    MUTE = "mute"

class Membership(Base):
    __tablename__ = "memberships"
    membership_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func())
    membership_type: Mapped[MembershipTypes] = mapped_column(default=MembershipTypes.MEMBER)
    notification_type: Mapped[NotificationTypes] = mapped_column(default=NotificationTypes.NOTIFY)

    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="unique_membership"),
    )

# contacts
class ContactStatus(enum.Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class ContactModel(BaseModel):
    contact_id: int
    nickname: str | None
    requested_at: datetime
    responded_at: datetime | None
    contact_status: ContactStatus

class Contact(Base):
    __tablename__ = "contacts"
    contact_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    contact_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    nickname: Mapped[str | None] = mapped_column(String(25), default=None)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=date_func())
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    contact_status: Mapped[ContactStatus] = mapped_column(default=ContactStatus.REQUESTED)
    conversation_id: Mapped[int | None] = mapped_column(
        ForeignKey("conversations.conversation_id"),
        nullable=True,
        default=None
    )

    __table_args__ = (
        UniqueConstraint("user_id", "contact_user_id", name="unique_contact"),
    )

    def clean_return(self) -> ContactModel:
        return ContactModel(
            contact_id=self.contact_id,
            nickname=self.nickname,
            requested_at=self.requested_at,
            responded_at=self.responded_at,
            contact_status=self.contact_status
        )