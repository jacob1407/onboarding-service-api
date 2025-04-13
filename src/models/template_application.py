from sqlalchemy import UUID, Column, ForeignKey

from ..db import Base


class TemplateApplicationModel(Base):
    __tablename__ = "template_applications"

    application_id = Column(
        UUID(as_uuid=True), ForeignKey("applications.id"), primary_key=True
    )
    template_id = Column(
        UUID(as_uuid=True), ForeignKey("templates.id"), primary_key=True
    )
