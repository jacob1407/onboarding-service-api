from sqlalchemy.orm import Session
from uuid import UUID
from ..data_access.role_templates_dao import RoleTemplateDAO


class RoleTemplateService:
    def __init__(self, db: Session):
        self.dao = RoleTemplateDAO(db)

    def associate_templates_to_role(
        self, role_id: UUID, template_ids: list[UUID]
    ) -> None:
        for template_id in template_ids:
            self.dao.create(role_id, template_id)

    def get_template_ids_for_role(self, role_id: UUID) -> list[UUID]:
        return self.dao.get_templates_by_role_id(role_id)
