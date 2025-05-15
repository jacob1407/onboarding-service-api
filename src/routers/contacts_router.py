from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.contact_schema import (
    CreateContactRequestModel,
    GetContactResponseModel,
)
from ..services.contacts_service import ContactService
from ..db import get_transactional_session

router = APIRouter()


@router.post("/", response_model=GetContactResponseModel)
def create_contact(
    data: CreateContactRequestModel, db: Session = Depends(get_transactional_session)
):
    service = ContactService(db)
    return service.create_contact(data)


@router.get("/", response_model=list[GetContactResponseModel])
def get_contacts(
    organisation_id: UUID, db: Session = Depends(get_transactional_session)
):
    service = ContactService(db)
    return service.get_contacts_by_org_id(organisation_id)


@router.get("/{contact_id}", response_model=GetContactResponseModel)
def get_contact(contact_id: UUID, db: Session = Depends(get_transactional_session)):
    service = ContactService(db)
    contact = service.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=GetContactResponseModel)
def update_contact(
    contact_id: UUID,
    data: CreateContactRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = ContactService(db)
    updated = service.update_contact(contact_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated


@router.delete("/{contact_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_contact(contact_id: UUID, db: Session = Depends(get_transactional_session)):
    service = ContactService(db)
    deleted = service.delete_contact(contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
