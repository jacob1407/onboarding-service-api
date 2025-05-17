from uuid import uuid4
from sqlalchemy import Column, DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from ..db.db import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
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
