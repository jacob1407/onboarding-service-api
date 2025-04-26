from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.applications_schema import GetApplicationsResponseModel
from ..data_access.role_application_data_access import RoleApplicationDataAccess


class RoleApplicationsService:
    def __init__(self, db: Session):
        self.dao = RoleApplicationDataAccess(db)

    def associate_applications_to_role(
        self, role_id: UUID, application_ids: list[UUID]
    ) -> None:
        for app_id in application_ids:
            self.dao.create(role_id, app_id)

    def get_application_ids_for_role(self, role_id: UUID) -> list[UUID]:
        return self.dao.get_application_ids_by_role_id(role_id)

    def get_applications_by_role_id(
        self, role_id: UUID
    ) -> list[GetApplicationsResponseModel]:
        applications = self.dao.get_all_applications_by_role_id(role_id)
        return [
            GetApplicationsResponseModel.model_validate(app) for app in applications
        ]

    def update_role_applications(
        self, role_id: UUID, new_application_ids: list[UUID]
    ) -> None:
        self.dao.update_role_applications(role_id, new_application_ids)
