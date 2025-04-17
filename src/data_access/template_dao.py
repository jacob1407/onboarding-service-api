from sqlalchemy.orm import Session
from ..models.template_model import TemplateModel
from ..schemas.templates_schema import CreateTemplateRequestModel
from uuid import UUID, uuid4


class TemplateDAO:
    def create(
        self, db: Session, template_data: CreateTemplateRequestModel
    ) -> TemplateModel:
        new_template = TemplateModel(
            id=uuid4(),
            name=template_data.name,
            display_name=template_data.display_name,
            organisation_id=template_data.organisation_id,
        )
        db.add(new_template)
        db.commit()
        db.refresh(new_template)
        return new_template

    def get_by_org(self, db: Session, org_id: UUID) -> list[TemplateModel]:
        return db.query(TemplateModel).filter_by(organisation_id=org_id).all()

    def update(
        self, db: Session, template_id: UUID, data: CreateTemplateRequestModel
    ) -> TemplateModel:
        template = db.query(TemplateModel).filter_by(id=template_id).one_or_none()
        template.name = data.name
        template.display_name = data.display_name
        template.organisation_id = data.organisation_id
        db.commit()
        db.refresh(template)
        return template

    def delete(self, db: Session, template_id: UUID) -> None:
        template = db.query(TemplateModel).filter_by(id=template_id).one_or_none()
        db.delete(template)
        db.commit()
