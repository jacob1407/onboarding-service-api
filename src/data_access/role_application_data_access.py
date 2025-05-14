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
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_application_ids_by_role_id(self, role_id: UUID) -> list[UUID]:
        return [
            r.application_id
            for r in self.db.query(RoleApplicationModel)
            .filter_by(role_id=role_id)
            .all()
        ]

    def update_role_applications(self, role_id: str, new_application_ids: list[str]):
        self.db.query(RoleApplicationModel).filter(
            RoleApplicationModel.role_id == role_id
        ).delete()
        self.db.bulk_save_objects(
            [
                RoleApplicationModel(role_id=role_id, application_id=app_id)
                for app_id in new_application_ids
            ]
        )
        self.db.commit()

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
