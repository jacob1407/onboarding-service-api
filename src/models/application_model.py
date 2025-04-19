import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class ApplicationModel(Base):
    __tablename__ = "applications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False, unique=False)
    description = Column(String, nullable=True)
    code = Column(String, nullable=False)
    organisation_id = Column(
        UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False
    )
