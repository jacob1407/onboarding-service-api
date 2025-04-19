from sqlalchemy.orm import Session
from uuid import UUID
from ..models.application_contact_model import ApplicationContactsModel


class ContactApplicationDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, application_id: UUID, contact_id: UUID
    ) -> ApplicationContactsModel:
        record = ApplicationContactsModel(
            application_id=application_id, contact_id=contact_id
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
