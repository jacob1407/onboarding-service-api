from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.contact_schema import (
    CreateContactRequestModel,
    GetContactResponseModel,
)
from ..services.contacts_service import ContactService
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=GetContactResponseModel)
def create_contact(data: CreateContactRequestModel, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.create_contact(data)


@router.get("/", response_model=list[GetContactResponseModel])
def get_contacts(org_id: UUID, db: Session = Depends(get_db)):
    service = ContactService(db)
    return service.get_contacts_by_org_id(org_id)


@router.get("/{contact_id}", response_model=GetContactResponseModel)
def get_contact(contact_id: UUID, db: Session = Depends(get_db)):
    service = ContactService(db)
    contact = service.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
