from sqlalchemy.orm import Session
from ..models.application_model import ApplicationModel
from ..schemas.applications_schema import CreateApplicationRequestModel
import uuid
from uuid import UUID


class ApplicationsDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateApplicationRequestModel) -> ApplicationModel:
        app = ApplicationModel(
            id=uuid.uuid4(),
            name=data.name,
            display_name=data.display_name,
            organisation_id=data.organisation_id,
        )
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def get_by_org_id(self, org_id: UUID) -> list[ApplicationModel]:
        return self.db.query(ApplicationModel).filter_by(organisation_id=org_id).all()

    def get_by_id(self, app_id: UUID) -> ApplicationModel | None:
        return self.db.query(ApplicationModel).filter_by(id=app_id).first()
