from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class ApplicationContactsModel(Base):
    __tablename__ = "application_contacts"

    application_id = Column(
        UUID(as_uuid=True), ForeignKey("applications.id"), primary_key=True
    )
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), primary_key=True)
