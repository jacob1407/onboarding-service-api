from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.contact_schema import (
    CreateContactRequestModel,
    GetContactResponseModel,
)
from ..data_access.contact_data_access import ContactDataAccess


class ContactService:
    def __init__(self, db: Session):
        self.dao = ContactDataAccess(db)

    def create_contact(
        self, data: CreateContactRequestModel
    ) -> GetContactResponseModel:
        contact = self.dao.create(data)
        return GetContactResponseModel.model_validate(contact)

    def get_contacts_by_org_id(self, org_id: UUID) -> list[GetContactResponseModel]:
        contacts = self.dao.get_by_org_id(org_id)
        return [GetContactResponseModel.model_validate(c) for c in contacts]

    def get_contact_by_id(self, contact_id: UUID) -> GetContactResponseModel | None:
        contact = self.dao.get_by_id(contact_id)
        return GetContactResponseModel.model_validate(contact) if contact else None

    def get_contacts_by_ids(
        self, contact_ids: list[UUID]
    ) -> list[GetContactResponseModel]:
        contacts = self.dao.get_by_ids(contact_ids)
        return [GetContactResponseModel.model_validate(c) for c in contacts]
