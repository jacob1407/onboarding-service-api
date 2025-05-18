from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.contact_schema import (
    CreateContactRequestModel,
    GetContactResponseModel,
)
from ..data_access.contact_data_access import ContactDataAccess
from ..data_access.application_contacts_data_access import ApplicationContactDataAccess


class ContactService:
    def __init__(self, db: Session):
        self.db = db
        self.data_access = ContactDataAccess(db)
        self.application_data_access = ApplicationContactDataAccess(db)

    def create_contact(
        self, data: CreateContactRequestModel, organisation_id: UUID
    ) -> GetContactResponseModel:
        contact = self.data_access.create(data, organisation_id)
        return GetContactResponseModel.model_validate(contact)

    def get_contacts_by_org_id(
        self, organisation_id: UUID
    ) -> list[GetContactResponseModel]:
        contacts = self.data_access.get_by_org_id(organisation_id)
        return [GetContactResponseModel.model_validate(c) for c in contacts]

    def get_contact_by_id(
        self, contact_id: UUID, organisation_id: UUID
    ) -> GetContactResponseModel | None:
        contact = self.data_access.get_by_id(contact_id)
        if not contact:
            return None

        if str(contact.organisation_id) != organisation_id:
            raise HTTPException(
                status_code=401, detail="User does not have access to view this contact"
            )
        return GetContactResponseModel.model_validate(contact)

    def get_contacts_by_ids(
        self, contact_ids: list[UUID]
    ) -> list[GetContactResponseModel]:
        contacts = self.data_access.get_by_ids(contact_ids)
        return [GetContactResponseModel.model_validate(c) for c in contacts]

    def update_contact(
        self, contact_id: UUID, data: CreateContactRequestModel, organisation_id: UUID
    ) -> GetContactResponseModel | None:
        contact = self.data_access.update(contact_id, data, organisation_id)
        if not contact:
            return None
        if str(contact.organisation_id) != organisation_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to update this contact",
            )
        return GetContactResponseModel.model_validate(contact)

    def delete_contact(self, contact_id: UUID, organisation_id: UUID) -> bool:
        contact = self.data_access.get_by_id(contact_id)
        if not contact:
            return False
        if str(contact.organisation_id) != organisation_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to delete this contact",
            )
        self.application_data_access.delete_by_contact_id(contact_id)
        self.data_access.delete_contact(contact_id)
        return True
