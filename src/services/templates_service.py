import re
from sqlalchemy.orm import Session
from uuid import UUID

from ..services.template_applications_service import TemplateApplicationsService

from ..schemas.templates_schema import (
    CreateTemplateRequestModel,
    TemplateResponseModel,
    UpdateTemplateRequestModel,
)
from ..data_access.template_dao import TemplateDAO


class TemplateService:
    def __init__(self, db: Session):
        self.dao = TemplateDAO(db)
        self.template_application_service = TemplateApplicationsService(db)

    def create_template(
        self, data: CreateTemplateRequestModel
    ) -> TemplateResponseModel:
        template = self.dao.create(data)

        if len(data.application_ids) > 0:
            self.template_application_service.associate_applications_to_template(
                template.id, data.application_ids
            )

        return TemplateResponseModel(
            id=template.id,
            name=template.name,
            code=template.code,
            organisation_id=template.organisation_id,
            application_ids=data.application_ids,
        )

    def get_templates_by_org(self, org_id: UUID) -> list[TemplateResponseModel]:
        templates = self.dao.get_by_org(org_id)
        return [TemplateResponseModel.model_validate(t) for t in templates]

    def update_template(
        self, template_id: UUID, data: UpdateTemplateRequestModel
    ) -> TemplateResponseModel:
        template = self.dao.update(template_id, data)

        if len(data.application_ids) > 0:
            self.template_application_service.associate_applications_to_template(
                template.id, data.application_ids
            )

        return TemplateResponseModel.model_validate(template)

    def delete_template(self, template_id: UUID) -> None:
        self.dao.delete(template_id)
