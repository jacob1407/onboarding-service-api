from sqlalchemy import UUID, Column, ForeignKey

from ..db import Base


class RoleTemplateModel(Base):
    __tablename__ = "role_templates"

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), primary_key=True)
    template_id = Column(
        UUID(as_uuid=True), ForeignKey("templates.id"), primary_key=True
    )
