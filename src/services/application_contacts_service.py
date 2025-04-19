from sqlalchemy.orm import Session
from uuid import UUID
from ..data_access.application_contacts_dao import ContactApplicationDAO


class ApplicationContactsService:
    def __init__(self, db: Session):
        self.dao = ContactApplicationDAO(db)

    def associate_contacts_to_application(
        self, application_id: UUID, contact_ids: list[UUID]
    ) -> None:
        for contact_id in contact_ids:
            self.dao.create(application_id, contact_id)
