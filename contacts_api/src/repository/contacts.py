from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas.contacts import ContactCreate, ContactUpdate
from datetime import  datetime, timedelta


def create_contact(db: Session, contact: ContactCreate):
    new_contact = Contact(**contact.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def get_contacts(db: Session):
    return db.query(Contact).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, data: ContactUpdate):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        for key, value in data.model_dump().items():
            setattr(contact, key, value)
        db.commit()
    return contact


def delete_contact(db: Session, contact_id: int):
    contact = get_contact_by_id(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


def search_contacts(query: str, db: Session):
    return (
        db.query(Contact)
        .filter(
            (Contact.first_name.ilike(f"%{query}%"))
            | (Contact.last_name.ilike(f"%{query}%"))
            | (Contact.email.ilike(f"%{query}%"))
        )
        .all()
    )


def upcoming_birthdays(db: Session):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()
