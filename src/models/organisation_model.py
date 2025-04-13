import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False)
    contact_emails = Column(String, nullable=False)
