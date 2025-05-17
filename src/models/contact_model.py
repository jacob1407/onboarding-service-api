from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from ..db.db import Base


class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=False)
    external_id = Column(String, nullable=True, unique=True)
    organisation_id = Column(
        UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False
    )
    created_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_updated_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
