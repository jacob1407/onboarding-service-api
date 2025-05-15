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
        self.data_access = ContactDataAccess(db)
        self.application_data_access = ApplicationContactDataAccess(db)

    def create_contact(
        self, data: CreateContactRequestModel
    ) -> GetContactResponseModel:
        contact = self.data_access.create(data)
        return GetContactResponseModel.model_validate(contact)

    def get_contacts_by_org_id(self, org_id: UUID) -> list[GetContactResponseModel]:
        contacts = self.data_access.get_by_org_id(org_id)
        return [GetContactResponseModel.model_validate(c) for c in contacts]

    def get_contact_by_id(self, contact_id: UUID) -> GetContactResponseModel | None:
        contact = self.data_access.get_by_id(contact_id)
        return GetContactResponseModel.model_validate(contact) if contact else None

    def get_contacts_by_ids(
        self, contact_ids: list[UUID]
    ) -> list[GetContactResponseModel]:
        contacts = self.data_access.get_by_ids(contact_ids)
        return [GetContactResponseModel.model_validate(c) for c in contacts]

    def update_contact(
        self, contact_id: UUID, data: CreateContactRequestModel
    ) -> GetContactResponseModel | None:
        contact = self.data_access.update(contact_id, data)
        return GetContactResponseModel.model_validate(contact) if contact else None

    def delete_contact(self, contact_id: UUID) -> bool:
        contact = self.data_access.get_by_id(contact_id)
        if not contact:
            return False
        self.application_data_access.delete_by_contact_id(contact_id)
        self.data_access.delete_contact(contact_id)
        return True
