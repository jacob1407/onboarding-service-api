from sqlalchemy.orm import Session

from ..services.applications_service import ApplicationService
from ..data_access.roles_dao import RolesDAO
from ..services.role_applications_service import RoleApplicationsService
from ..schemas.roles_schema import (
    CreateRoleRequestModel,
    GetRoleResponseModel,
    GetRolesResponseModel,
)


class RolesService:
    def __init__(self, db: Session):
        self.__dao = RolesDAO(db)
        self.__role_application_service = RoleApplicationsService(db)
        self.applications_service = ApplicationService(db)

    def create_role(self, data: CreateRoleRequestModel) -> GetRolesResponseModel:
        role = self.__dao.create_role(data)

        if len(data.application_ids) > 0:
            self.__role_application_service.associate_applications_to_role(
                role.id, data.application_ids
            )

        return GetRolesResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            application_ids=data.application_ids,
            description=role.description,
            organisation_id=role.organisation_id,
        )

    def get_all_roles_by_org_id(self, org_id: str) -> list[GetRolesResponseModel]:
        roles = self.__dao.get_all_roles_by_org_id(org_id)
        return [GetRolesResponseModel.model_validate(r) for r in roles]

    def get_role_by_id(self, role_id: str) -> GetRolesResponseModel | None:
        role = self.__dao.get_role_by_id(role_id)
        if not role:
            return None

        application_ids = self.__role_application_service.get_application_ids_for_role(
            role_id
        )

        applications = []
        if application_ids:
            applications = self.applications_service.get_applications_by_ids(
                application_ids
            )

        return GetRoleResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            description=role.description,
            applications=applications,
        )

    def update_role(
        self, role_id: str, data: CreateRoleRequestModel
    ) -> GetRolesResponseModel | None:
        role = self.__dao.get_role_by_id(role_id)
        if not role:
            return None

        updated_role = self.__dao.update_role(role_id, data)
        self.__role_application_service.update_role_applications(
            role_id, data.application_ids
        )

        applications = self.applications_service.get_applications_by_ids(
            data.application_ids
        )

        return GetRoleResponseModel(
            id=updated_role.id,
            name=updated_role.name,
            code=updated_role.code,
            description=updated_role.description,
            applications=applications,
        )
