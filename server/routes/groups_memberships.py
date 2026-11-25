from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pydantic import BaseModel
from datetime import datetime

from database import get_db, add_to_db
from models import (
    User, UserModel,
    Group, GroupModel,
    Membership, MembershipTypes,
    Conversation
)
from routes import helpers

router = APIRouter(prefix="/group", tags=["group"])

# POST /group/create_group
class CreateGroupModel(BaseModel):
    group_name: str
    description: str

@router.post("/create_group")
async def create_group(
    group: CreateGroupModel,
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> GroupModel:                            # create a new group with the current user as admin
    try:
        db_conversation = Conversation()
        await add_to_db(db_conversation, db, commit=False)
        
        db_group = Group(
            group_name = group.group_name,
            description = group.description,
            conversation_id = db_conversation.conversation_id
        )
        await add_to_db(db_group, db, commit=False)

        db_membership = Membership(
            user_id = user.user_id,
            group_id = db_group.group_id,
            membership_type = MembershipTypes.ADMIN
        )
        await add_to_db(db_membership, db, commit=False)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error when creating group. Please try again"
        ) from exc

    return db_group.clean_return()


# GET /get_groups
class MemberGroup(BaseModel):
    group: GroupModel
    membership_type: MembershipTypes

@router.get("/get_groups")
async def get_groups(
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[MemberGroup]:                     # get all the groups the current user is a member of

    db_groups = (await db.execute(
        select(Group, Membership.membership_type)
        .join(Membership, Membership.group_id == Group.group_id)
        .where(Membership.user_id == user.user_id)
    )).all()

    return [
        MemberGroup(
            group=group.clean_return(),
            membership_type=membership_type
        ) for group, membership_type in db_groups
    ]


# GET /group-{group_id}/get_group_members
class GroupMember(BaseModel):
    user: UserModel
    membership_type: MembershipTypes
    joined_at: datetime

@router.get("/group-{group_id}/get_group_members")
async def get_group_members(
    group_id: int,
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> list[GroupMember]:                                 # get all the members of the given group if the current user is a member
    check = await db.scalar(select(Membership).where(
        Membership.group_id == group_id,
        Membership.user_id == user.user_id
    ))
    if check == None: raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail="Group not found"
    )

    db_members = (await db.execute(
        select(User, Membership)
        .join(Membership, Membership.user_id == User.user_id)
        .where(Membership.group_id == group_id)
    )).all()

    return [
        GroupMember(
            user=db_user.clean_return(),
            membership_type=db_membership.membership_type,
            joined_at=db_membership.joined_at
        ) for db_user, db_membership in db_members
    ]