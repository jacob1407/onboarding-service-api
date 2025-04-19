from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from ..schemas.templates_schema import (
    CreateTemplateRequestModel,
    UpdateTemplateRequestModel,
)
from ..models.template_model import TemplateModel
from uuid import UUID, uuid4


class TemplateDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, template: CreateTemplateRequestModel) -> TemplateModel:
        new_template = TemplateModel(
            id=uuid4(),
            name=template.name,
            code=template.code,
            organisation_id=template.organisation_id,
        )
        self.db.add(new_template)
        self.db.commit()
        self.db.refresh(new_template)
        return new_template

    def get_by_org(self, org_id: UUID) -> list[TemplateModel]:
        return self.db.query(TemplateModel).filter_by(organisation_id=org_id).all()

    def update(
        self, template_id: UUID, template: UpdateTemplateRequestModel
    ) -> TemplateModel:
        template = self.db.query(TemplateModel).filter_by(id=template_id).one_or_none()
        if not template:
            raise NoResultFound(f"Template {template.id} not found")
        template.name = template.name
        template.code = template.code
        self.db.commit()
        self.db.refresh(template)
        return template

    def delete(self, template_id: UUID) -> None:
        template = self.db.query(TemplateModel).filter_by(id=template_id).one_or_none()
        if not template:
            raise NoResultFound(f"Template {template_id} not found")
        self.db.delete(template)
        self.db.commit()
