import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=False)
