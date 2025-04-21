from sqlalchemy.orm import Session
from uuid import UUID
from ..data_access.role_applications_dao import RoleApplicationDAO


class RoleApplicationsService:
    def __init__(self, db: Session):
        self.dao = RoleApplicationDAO(db)

    def associate_applications_to_role(
        self, role_id: UUID, application_ids: list[UUID]
    ) -> None:
        for app_id in application_ids:
            self.dao.create(role_id, app_id)

    def get_application_ids_for_role(self, role_id: UUID) -> list[UUID]:
        return self.dao.get_applications_by_role_id(role_id)
