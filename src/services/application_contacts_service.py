from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.user_schema import GetUserResponseModel

from ..data_access.application_contacts_data_access import ApplicationContactDataAccess


class ApplicationContactsService:
    def __init__(self, db: Session):
        self.dao = ApplicationContactDataAccess(db)

    def associate_contacts_to_application(
        self, application_id: UUID, contact_ids: list[UUID]
    ) -> None:
        for contact_id in contact_ids:
            self.dao.create(application_id, contact_id)

    def get_contacts_by_application_id(
        self, application_id: UUID
    ) -> list[GetUserResponseModel]:
        contacts = self.dao.get_all_contacts_by_application_id(application_id)
        return [GetUserResponseModel.model_validate(contact) for contact in contacts]

    def update_application_contacts(
        self, application_id: UUID, contact_ids: list[UUID]
    ) -> None:
        self.dao.update_application_contacts(application_id, contact_ids)
