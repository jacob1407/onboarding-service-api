import uuid
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from ..db.db import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False, unique=True)
    contact_emails = Column(String, nullable=False)
    created_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_updated_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
