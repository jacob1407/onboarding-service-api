from sqlalchemy.orm import Session
from uuid import UUID
from ..models.contact_model import ContactModel
from ..schemas.contact_schema import CreateContactRequestModel
import uuid


class ContactDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateContactRequestModel) -> ContactModel:
        contact = ContactModel(
            id=uuid.uuid4(),
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            external_id=data.external_id,
            organisation_id=data.organisation_id,
        )
        self.db.add(contact)
        self.db.flush()
        return contact

    def get_by_org_id(self, org_id: UUID) -> list[ContactModel]:
        return (
            self.db.query(ContactModel)
            .filter(ContactModel.organisation_id == org_id)
            .all()
        )

    def get_by_id(self, contact_id: UUID) -> ContactModel | None:
        return self.db.query(ContactModel).filter(ContactModel.id == contact_id).first()

    def get_by_ids(self, contact_ids: list[UUID]) -> list[ContactModel]:
        return (
            self.db.query(ContactModel).filter(ContactModel.id.in_(contact_ids)).all()
        )

    def update(
        self, contact_id: UUID, data: CreateContactRequestModel
    ) -> ContactModel | None:
        contact = (
            self.db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        )
        if not contact:
            return None

        contact.first_name = data.first_name
        contact.last_name = data.last_name
        contact.email = data.email
        return contact

    def delete_contact(self, contact_id: UUID):
        contact = (
            self.db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        )
        if contact:
            self.db.delete(contact)
