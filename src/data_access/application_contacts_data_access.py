from sqlalchemy.orm import Session
from uuid import UUID

from ..models.contact_model import ContactModel
from ..models.application_contact_model import ApplicationContactsModel


class ApplicationContactDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, application_id: UUID, contact_id: UUID
    ) -> ApplicationContactsModel:
        record = ApplicationContactsModel(
            application_id=application_id, contact_id=contact_id
        )
        self.db.add(record)
        self.db.flush()
        return record

    def get_contact_ids_by_application_id(self, application_id: UUID) -> list[UUID]:
        records = (
            self.db.query(ApplicationContactsModel)
            .filter(ApplicationContactsModel.application_id == application_id)
            .all()
        )
        return [record.contact_id for record in records]

    def get_all_contacts_by_application_id(
        self, application_id: UUID
    ) -> list[ContactModel]:
        return (
            self.db.query(ContactModel)
            .join(
                ApplicationContactsModel,
                ApplicationContactsModel.contact_id == ContactModel.id,
            )
            .filter(ApplicationContactsModel.application_id == application_id)
            .all()
        )

    def update_application_contacts(
        self, application_id: str, new_contact_ids: list[str]
    ):
        self.db.query(ApplicationContactsModel).filter(
            ApplicationContactsModel.application_id == application_id
        ).delete()
        self.db.bulk_save_objects(
            [
                ApplicationContactsModel(
                    application_id=application_id, contact_id=contact_id
                )
                for contact_id in new_contact_ids
            ]
        )

    def delete_by_contact_id(self, contact_id: UUID):
        self.db.query(ApplicationContactsModel).filter(
            ApplicationContactsModel.contact_id == contact_id
        ).delete()

    def delete_by_application_id(self, application_id: UUID):
        self.db.query(ApplicationContactsModel).filter(
            ApplicationContactsModel.application_id == application_id
        ).delete()
