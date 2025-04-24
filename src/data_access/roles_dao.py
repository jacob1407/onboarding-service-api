from uuid import UUID
from sqlalchemy.orm import Session

from ..schemas.roles_schema import CreateRoleRequestModel
from ..models.role_model import RoleModel


class RolesDAO:
    def __init__(self, db: Session):
        self.db = db

    def create_role(self, role: CreateRoleRequestModel) -> RoleModel:
        role = RoleModel(
            name=role.name,
            code=role.code,
            organisation_id=role.organisation_id,
            description=role.description,
        )
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def get_all_roles_by_org_id(self, org_id: str) -> list[RoleModel]:
        return (
            self.db.query(RoleModel).filter(RoleModel.organisation_id == org_id).all()
        )

    def get_role_by_id(self, role_id: str) -> RoleModel | None:
        return self.db.query(RoleModel).filter(RoleModel.id == role_id).first()

    def update_role(self, role_id: str, data: CreateRoleRequestModel) -> RoleModel:
        role = self.get_role_by_id(role_id)
        role.name = data.name
        role.description = data.description
        self.db.commit()
        self.db.refresh(role)
        return role
