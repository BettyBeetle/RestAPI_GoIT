from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, extract

from typing import List
from datetime import datetime, timedelta

from m11.database.models import Contacts
from m11.schemas import ContactsIn


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contacts]:
    return db.query(Contacts).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contacts:
    return db.query(Contacts).filter(Contacts.id == contact_id).first()


async def create_contact(body: ContactsIn, db: Session) -> Contacts:
    contact = Contacts(
        first_name = body.first_name,
        last_name = body.last_name,
        email = body.email,
        phone_number = body.phone_number,
        date_of_birth = body.date_of_birth,
        nick = body.nick,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactsIn, db: Session) -> Contacts | None:
    contact = db.query(Contacts).filter(Contacts.id == contact_id).first()
    if contact:
        if body.first_name:
            contact.first_name = body.first_name
        if body.last_name:
            contact.last_name = body.last_name
        if body.email is not None:
            contact.email = body.email
        if body.phone_number:
            contact.phone_number = body.phone_number
        if body.date_of_birth:
            contact.date_of_birth = body.date_of_birth
        if body.nick is not None:
            contact.nick = body.nick
        db.commit()
        return contact


async def search_contacts(search: str, skip: int, limit: int, db: Session):

    search_terms = search.split()

    conditions = [or_(
        Contacts.first_name.ilike(f'%{term}%'),
        Contacts.last_name.ilike(f'%{term}%'),
        Contacts.email.ilike(f'%{term}%')
    ) for term in search_terms]

    search_query = or_(*conditions)
    contacts = db.query(Contacts).filter(search_query).offset(skip).limit(limit).all()

    return contacts


async def upcoming_birthdays(db: Session) -> List[Contacts]:
    today = datetime.now().date()
    end_date = today + timedelta(days=7)

    if today.month == end_date.month:
        contacts = db.query(Contacts).filter(
            extract('month', Contacts.date_of_birth) == today.month,
            extract('day', Contacts.date_of_birth) >= today.day,
            extract('day', Contacts.date_of_birth) <= end_date.day
        ).all()
    else:
        contacts = db.query(Contacts).filter(
            or_(
                and_(
                    extract('month', Contacts.date_of_birth) == today.month,
                    extract('day', Contacts.date_of_birth) >= today.day
                ),
                and_(
                    extract('month', Contacts.date_of_birth) == end_date.month,
                    extract('day', Contacts.date_of_birth) <= end_date.day
                )
            )
        ).all()

    return contacts
