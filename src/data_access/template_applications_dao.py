from sqlalchemy.orm import Session
from uuid import UUID
from ..models.template_application_model import TemplateApplicationModel


class TemplateApplicationDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self, template_id: UUID, application_id: UUID
    ) -> TemplateApplicationModel:
        record = TemplateApplicationModel(
            template_id=template_id, application_id=application_id
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
