from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.contacts import *
from src.database.db import get_db
from src.repository import contacts as repo

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse)
def create(contact: ContactCreate, db: Session = Depends(get_db)):
    return repo.create_contact(db, contact)

@router.get("/", response_model=List[ContactResponse])
def read_all(db: Session = Depends(get_db)):
    return repo.get_contacts(db)

@router.get("/{contact_id}", response_model=ContactResponse)
def read_one(contact_id: int, db: Session = Depends(get_db)):
    contact = repo.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    return repo.update_contact(db, contact_id, contact)


@router.delete("/{contact_id}", response_model=ContactResponse)
def delete(contact_id: int, db: Session = Depends(get_db)):
    return repo.delete_contact(db, contact_id)

@router.get("/search/{query}", response_model=List[ContactResponse])
def search(query: str, db: Session = Depends(get_db)):
    return repo.search_contacts(query, db)

@router.get("/birthdays/upcoming", response_model=List[ContactResponse])
def birthdays(db: Session = Depends(get_db)):
    return repo.upcoming_birthdays(db)

