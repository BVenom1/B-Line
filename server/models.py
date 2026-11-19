'''
This is the file where the ORM models and pydantic scemas
related to the database tables are defined.
'''
from database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, false, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import CITEXT

from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime
import enum

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
        clean_user = self.model_copy()
        clean_user.password = None
        return clean_user

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

# conversations:
class Conversation(Base):
    __tablename__ = "conversations"
    conversation_id: Mapped[int] = mapped_column(primary_key=True)

# groups:
class GroupModel(BaseModel):
    group_id: int | None = None
    group_name: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    conversation_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

    def clean_return(self) -> GroupModel:
        clean_group = self.model_copy()
        clean_group.conversation_id = None
        return clean_group

class Group(Base):
    __tablename__ = "groups"
    group_id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    conversation_id: Mapped[int | None] = mapped_column(
        ForeignKey("conversations.conversation_id", ondelete="SET NULL"),
        nullable=True
    )

    @classmethod
    def from_scema(cls, group: GroupModel) -> Group:
        return Group(
            group_id = group.group_id,
            group_name = group.group_name,
            description = group.description,
            created_at = group.created_at or datetime.now().astimezone(),
            conversation_id = group.conversation_id
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

class MembershipModel(BaseModel):
    membership_id: int | None = None
    user_id: int | None = None
    group_id: int | None = None
    joined_at: datetime | None = None
    membership_type: MembershipTypes = MembershipTypes.MEMBER
    notification_type: NotificationTypes | None = None

    model_config = ConfigDict(from_attributes=True)

    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="unique_membership")
    )

    def clean_return(self) -> MembershipModel:
        clean_membership = self.model_copy()
        clean_membership.notification_type = None
        return clean_membership

class Membership(Base):
    __tablename__ = "memberships"
    membership_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    membership_type: Mapped[MembershipTypes] = mapped_column(default=MembershipTypes.MEMBER)
    notification_type: Mapped[NotificationTypes] = mapped_column(default=NotificationTypes.NOTIFY)

    @classmethod
    def from_schema(cls, membership: MembershipModel) -> Membership:
        return Membership(
            membership_id = membership.membership_id,
            user_id = membership.user_id,
            group_id = membership.group_id,
            joined_at = membership.joined_at or datetime.now().astimezone(),
            membership_type = membership.membership_type,
            notification_type = membership.notification_type or NotificationTypes.NOTIFY
        )