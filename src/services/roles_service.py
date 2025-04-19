from sqlalchemy.orm import Session

from ..services.utils import to_snake_case
from ..data_access.roles_dao import RolesDAO
from ..services.role_templates_service import RoleTemplateService
from ..schemas.roles_schema import CreateRoleRequestModel, GetRolesResponseModel


class RolesService:
    def __init__(self, db: Session):
        self.dao = RolesDAO(db)
        self.role_template_service = RoleTemplateService(db)

    def create_role(self, data: CreateRoleRequestModel) -> GetRolesResponseModel:
        role = self.dao.create_role(data)

        if len(data.template_ids) > 0:
            self.role_template_service.associate_templates_to_role(
                role.id, data.template_ids
            )

        return GetRolesResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            template_ids=data.template_ids,
            organisation_id=role.organisation_id,
        )

    def get_all_roles_by_org_id(self, org_id: str) -> list[GetRolesResponseModel]:
        roles = self.dao.get_all_roles_by_org_id(org_id)
        return [GetRolesResponseModel.model_validate(r) for r in roles]

    def get_role_by_id(self, role_id: str) -> GetRolesResponseModel | None:
        role = self.dao.get_role_by_id(role_id)
        if not role:
            return None

        template_ids = self.role_template_service.get_template_ids_for_role(role_id)
        response = GetRolesResponseModel(
            id=role.id,
            name=role.name,
            code=role.code,
            organisation_id=role.organisation_id,
            template_ids=template_ids,
        )
        return response
