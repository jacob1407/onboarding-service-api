from uuid import UUID
from sqlalchemy.orm import Session


from ..models.application_model import ApplicationModel
from ..models.role_application_model import RoleApplicationModel


class RoleApplicationDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create(self, role_id: UUID, application_id: UUID) -> RoleApplicationModel:
        record = RoleApplicationModel(role_id=role_id, application_id=application_id)
        self.db.add(record)
        self.db.flush()
        return record

    def get_application_ids_by_role_id(self, role_id: UUID) -> list[UUID]:
        rows = (
            self.db.query(RoleApplicationModel.application_id)
            .filter_by(role_id=role_id)
            .all()
        )
        return [row.application_id for row in rows]

    def update_role_applications(self, role_id: UUID, new_application_ids: list[UUID]):
        self.db.query(RoleApplicationModel).filter(
            RoleApplicationModel.role_id == role_id
        ).delete()
        self.db.bulk_save_objects(
            [
                RoleApplicationModel(role_id=role_id, application_id=app_id)
                for app_id in new_application_ids
            ]
        )

    def get_all_applications_by_role_id(self, role_id: UUID) -> list[ApplicationModel]:
        return (
            self.db.query(ApplicationModel)
            .join(
                RoleApplicationModel,
                RoleApplicationModel.application_id == ApplicationModel.id,
            )
            .filter(RoleApplicationModel.role_id == role_id)
            .all()
        )

    def delete_by_application_id(self, application_id: UUID):
        self.db.query(RoleApplicationModel).filter(
            RoleApplicationModel.application_id == application_id
        ).delete()
