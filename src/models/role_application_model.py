from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..db.db import Base


class RoleApplicationModel(Base):
    __tablename__ = "role_applications"

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    application_id = Column(
        UUID(as_uuid=True), ForeignKey("applications.id"), primary_key=True
    )
