from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.contact_schema import GetContactResponseModel
from ..data_access.application_contacts_dao import ContactApplicationDAO


class ApplicationContactsService:
    def __init__(self, db: Session):
        self.dao = ContactApplicationDAO(db)

    def associate_contacts_to_application(
        self, application_id: UUID, contact_ids: list[UUID]
    ) -> None:
        for contact_id in contact_ids:
            self.dao.create(application_id, contact_id)

    def get_contacts_by_application_id(
        self, application_id: UUID
    ) -> list[GetContactResponseModel]:
        contacts = self.dao.get_all_contacts_by_application_id(application_id)
        return [GetContactResponseModel.model_validate(contact) for contact in contacts]

    def update_application_contacts(
        self, application_id: UUID, contact_ids: list[UUID]
    ) -> None:
        self.dao.update_application_contacts(application_id, contact_ids)
