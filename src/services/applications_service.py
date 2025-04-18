from sqlalchemy.orm import Session
from ..schemas.applications_schema import (
    CreateApplicationRequestModel,
    GetApplicationResponseModel,
)
from ..data_access.applications_dao import ApplicationsDAO
from ..models.application_model import ApplicationModel
from uuid import UUID


class ApplicationService:
    def __init__(self, db: Session):
        self.dao = ApplicationsDAO(db)

    def create_application(
        self, data: CreateApplicationRequestModel
    ) -> GetApplicationResponseModel:
        app = self.dao.create(data)
        return GetApplicationResponseModel.model_validate(app)

    def get_applications_by_org_id(
        self, org_id: UUID
    ) -> list[GetApplicationResponseModel]:
        apps = self.dao.get_by_org_id(org_id)
        return [GetApplicationResponseModel.model_validate(app) for app in apps]

    def get_application_by_id(self, app_id: UUID) -> GetApplicationResponseModel | None:
        app = self.dao.get_by_id(app_id)
        return GetApplicationResponseModel.model_validate(app) if app else None
