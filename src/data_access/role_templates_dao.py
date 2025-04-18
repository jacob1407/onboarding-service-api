from sqlalchemy.orm import Session
from ..models.role_template_model import RoleTemplateModel
from uuid import UUID


class RoleTemplateDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, role_id: UUID, template_id: UUID) -> RoleTemplateModel:
        association = RoleTemplateModel(role_id=role_id, template_id=template_id)
        self.db.add(association)
        self.db.commit()
        self.db.refresh(association)
        return association

    def get_templates_by_role_id(self, role_id: UUID) -> list[UUID]:
        return [
            r.template_id
            for r in self.db.query(RoleTemplateModel).filter_by(role_id=role_id).all()
        ]
