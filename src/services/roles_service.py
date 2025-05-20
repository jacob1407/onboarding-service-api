from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..services.applications_service import ApplicationService
from ..data_access.role_data_access import RoleDataAccess
from ..services.role_applications_service import RoleApplicationsService
from ..schemas.roles_schema import (
    CreateRoleRequestModel,
    GetRoleResponseModel,
    GetRolesResponseModel,
)


class RolesService:
    def __init__(self, db: Session):
        self.__data_access = RoleDataAccess(db)
        self.__role_application_service = RoleApplicationsService(db)
        self.applications_service = ApplicationService(db)

    def create_role(
        self, data: CreateRoleRequestModel, org_id: UUID
    ) -> GetRoleResponseModel:
        role = self.__data_access.create_role(data, org_id)

        if len(data.application_ids) > 0:
            self.__role_application_service.associate_applications_to_role(
                role.id, data.application_ids
            )
        applications = self.__role_application_service.get_applications_by_role_id(role)

        return GetRoleResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            applications=applications,
            description=role.description,
        )

    def get_all_roles_by_org_id(self, org_id: str) -> list[GetRolesResponseModel]:
        roles = self.__data_access.get_all_roles_by_org_id(org_id)
        return [GetRolesResponseModel.model_validate(r) for r in roles]

    def get_role_by_id(self, role_id: UUID) -> GetRolesResponseModel:
        role = self.__data_access.get_role_by_id(role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return GetRolesResponseModel.model_validate(role)

    def get_role_details_by_id(
        self, role_id: UUID, auth_organisation_id: str
    ) -> GetRoleResponseModel | None:
        role = self.__data_access.get_role_by_id(role_id)
        if not role:
            return None

        if str(role.organisation_id) != auth_organisation_id:
            raise HTTPException(
                status_code=401, detail="User does not have access to view this role"
            )

        applications = self.__role_application_service.get_applications_by_role_id(
            role_id
        )

        return GetRoleResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            description=role.description,
            applications=applications,
        )

    def update_role(
        self, role_id: UUID, data: CreateRoleRequestModel, auth_organisation_id: str
    ) -> GetRoleResponseModel | None:
        role = self.__data_access.get_role_by_id(role_id)
        if not role:
            return None

        if str(role.organisation_id) != auth_organisation_id:
            raise HTTPException(
                status_code=401, detail="User does not have access to update this role"
            )

        updated_role = self.__data_access.update_role(role_id, data)
        self.__role_application_service.update_role_applications(
            role_id, data.application_ids
        )

        applications = self.__role_application_service.get_applications_by_role_id(
            role_id
        )

        return GetRoleResponseModel(
            id=updated_role.id,
            name=updated_role.name,
            code=updated_role.code,
            description=updated_role.description,
            applications=applications,
        )
