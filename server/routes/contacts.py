from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from pydantic import BaseModel
from datetime import datetime, timezone

from models import (
    User, UserModel,
    Contact, ContactModel, ContactStatus,
    Conversation,
)
from database import get_db, add_to_db

from routes import helpers

router = APIRouter(prefix="/contact", tags=["contact"])

# POST /add_contact
class AddContactInputModel(BaseModel):
    email_or_uname: str

class UserContactModel(BaseModel):
    contact_user: UserModel
    contact: ContactModel

@router.post("/add_contact")
async def add_contact(
    input: AddContactInputModel,
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserContactModel:
    email_or_uname = input.email_or_uname.strip()
    contact_user = await db.scalar(select(User).where(or_(
        User.user_name == email_or_uname,
        User.email == email_or_uname.lower()
    )))
    if contact_user is None: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail="Given username/email is not registered"
    )
    elif contact_user.user_id == user.user_id: raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        detail="Cannot add yourself as a contact"
    )

    check = await db.scalar(select(Contact).where(
        Contact.user_id == user.user_id,
        Contact.contact_user_id == contact_user.user_id
    ))
    if check is not None: raise HTTPException(      # TODO: enable re-requesting if the previous request was rejected
        status.HTTP_409_CONFLICT,
        detail="You have already requested this account to be a contact"
    )

    check = await db.scalar(select(Contact).where(
        Contact.user_id == contact_user.user_id,
        Contact.contact_user_id == user.user_id
    ))
    if check is not None: raise HTTPException(
        status.HTTP_409_CONFLICT,
        detail="Given account has either already sent you a contact request, or you are blocked"
    )

    db_contact = Contact(
        user_id=user.user_id,
        contact_user_id=contact_user.user_id,
        nickname=contact_user.user_name,
    )
    await add_to_db(db_contact, db, lambda: HTTPException(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error creating contact. Please try again"
    ), commit=True)

    return UserContactModel(
        contact_user=contact_user.clean_return(),
        contact=db_contact.clean_return()
    )

# PATCH /accept_contact_request
class ContactInputModel(BaseModel):
    contact_id: int

@router.patch("/accept_contact_request")
async def accept_contact_request(
    input: ContactInputModel,
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserContactModel:
    # fetch the contact request
    db_contact = await helpers.get_contact(
        db, input.contact_id,
        contact_user=user,
        contact_status=ContactStatus.REQUESTED
    )

    # fetch the user related to the contact request
    db_contact_user = await db.scalar(select(User).where(
        User.user_id == db_contact.user_id
    ))
    if db_contact_user is None: raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        detail="Requesting user not found"
    )

    try:
        # get current time
        current_time = datetime.now(timezone.utc)

        # create a conversation
        db_conversation = Conversation()
        await add_to_db(db_conversation, db, commit=False)

        # update the contact request
        db_contact.contact_status = ContactStatus.ACCEPTED
        db_contact.responded_at = current_time
        db_contact.conversation_id = db_conversation.conversation_id
        await db.flush()

        # create a complementary contact for the current user
        new_db_contact = Contact(
            user_id = user.user_id,
            contact_user_id = db_contact.user_id,
            nickname = db_contact_user.user_name,
            requested_at = db_contact.requested_at,
            responded_at = current_time,
            contact_status = ContactStatus.ACCEPTED,
            conversation_id = db_conversation.conversation_id
        )
        await add_to_db(new_db_contact, db, commit=True)

    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error accepting contact request. Please try again"
        ) from exc

    return UserContactModel(
        contact_user= db_contact_user.clean_return(),
        contact= new_db_contact.clean_return()
    )

# PATCH /reject_contact_request
@router.patch("/reject_contact_request")
async def reject_contact_request(
    input: ContactInputModel,
    user: User = Depends(helpers.get_current_user),
    db: AsyncSession = Depends(get_db)
) -> UserContactModel:
    db_contact = await helpers.get_contact(
        db, input.contact_id,
        contact_user=user,
        contact_status=ContactStatus.REQUESTED
    )

    db_requester = await db.scalar(
        select(User)
        .where(User.user_id == db_contact.user_id)
    )
    if db_requester is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Contact not found"
        )

    try:
        db_contact.contact_status = ContactStatus.REJECTED
        db_contact.responded_at = datetime.now(timezone.utc)

        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to reject contact request. Please try again"
        )
    return UserContactModel(
        contact_user=db_requester.clean_return(),
        contact=db_contact.clean_return()
    )