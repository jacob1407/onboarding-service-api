from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.templates_schema import (
    CreateTemplateRequestModel,
    GetTemplateReturnModel,
)
from ..data_access.template_dao import TemplateDAO
from ..models.template_model import TemplateModel


class TemplateService:
    def __init__(self):
        self.dao = TemplateDAO()

    def create_template(
        self, db: Session, template_data: CreateTemplateRequestModel
    ) -> GetTemplateReturnModel:
        template = self.dao.create(db, template_data)
        return GetTemplateReturnModel.model_validate(template)

    def get_templates_by_org(
        self, db: Session, org_id: UUID
    ) -> list[GetTemplateReturnModel]:
        templates = self.dao.get_by_org(db, org_id)
        return [GetTemplateReturnModel.model_validate(t) for t in templates]

    def update_template(
        self, db: Session, template_id: UUID, data: CreateTemplateRequestModel
    ) -> GetTemplateReturnModel:
        template = self.dao.update(db, template_id, data)
        return GetTemplateReturnModel.model_validate(template)

    def delete_template(self, db: Session, template_id: UUID) -> None:
        self.dao.delete(db, template_id)
