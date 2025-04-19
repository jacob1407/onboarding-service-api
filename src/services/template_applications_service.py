from sqlalchemy.orm import Session
from uuid import UUID
from ..data_access.template_applications_dao import TemplateApplicationDAO


class TemplateApplicationsService:
    def __init__(self, db: Session):
        self.dao = TemplateApplicationDAO(db)

    def associate_applications_to_template(
        self, template_id: UUID, application_ids: list[UUID]
    ):
        for app_id in application_ids:
            self.dao.create(template_id, app_id)
