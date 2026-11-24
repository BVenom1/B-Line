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

    def clean_return(self) -> UserModel:
        return UserModel(
            user_name=self.user_name,
            email=self.email,
            status=self.status,
            is_verified=self.is_verified,
            created_at=self.created_at,
            verified_at=self.verified_at
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

    def clean_return(self) -> GroupModel:
        return GroupModel(
            group_name=self.group_name,
            description=self.description,
            created_at=self.created_at
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

class Membership(Base):
    __tablename__ = "memberships"
    membership_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.group_id"))
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    membership_type: Mapped[MembershipTypes] = mapped_column(default=MembershipTypes.MEMBER)
    notification_type: Mapped[NotificationTypes] = mapped_column(default=NotificationTypes.NOTIFY)

    __table_args__ = (
        UniqueConstraint("user_id", "group_id", name="unique_membership")
    )

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

    def clean_return(self) -> MembershipModel:
        return MembershipModel(
            user_id=self.user_id,
            group_id=self.group_id,
            joined_at=self.joined_at,
            membership_type=self.membership_type
        )

# contacts
class ContactStatus(enum.Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    BLOCKED = "blocked"

class ContactModel(BaseModel):
    contact_id: int | None = None
    user_id: int | None = None
    contact_user_id: int | None = None
    nickname: str | None = None
    requested_at: datetime | None = None
    responded_at: datetime | None = None
    contact_status: ContactStatus = ContactStatus.REQUESTED
    conversation_id: int | None = None

class Contact(Base):
    contact_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    contact_user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    nickname: Mapped[str | None] = mapped_column(String(25))
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    responded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    contact_status: Mapped[ContactStatus] = mapped_column(default=ContactStatus.REQUESTED)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.conversation_id"))

    @classmethod
    def from_schema(cls, contact: ContactModel) -> Contact:
        return Contact(
            contact_id = contact.contact_id,
            user_id = contact.user_id,
            contact_user_id = contact.contact_user_id,
            nickname = contact.nickname,
            requested_at = contact.requested_at or datetime.now().astimezone(),
            responded_at = contact.responded_at,
            contact_status = contact.contact_status,
            conversation_id = contact.conversation_id
        )

    def clean_return(self) -> ContactModel:
        return ContactModel(
            user_id=self.user_id,
            contact_user_id=self.contact_user_id,
            nickname=self.nickname,
            contact_status=self.contact_status
        )