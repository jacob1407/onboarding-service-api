from sqlalchemy.orm import Session

from ..services.utils import to_snake_case
from ..models.application_model import ApplicationModel
from ..schemas.applications_schema import CreateApplicationRequestModel
import uuid
from uuid import UUID


class ApplicationDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CreateApplicationRequestModel) -> ApplicationModel:
        app = ApplicationModel(
            id=uuid.uuid4(),
            name=data.name,
            code=to_snake_case(data.name),
            organisation_id=data.organisation_id,
            description=data.description,
        )
        self.db.add(app)
        self.db.commit()
        self.db.refresh(app)
        return app

    def get_by_org_id(self, org_id: UUID) -> list[ApplicationModel]:
        return self.db.query(ApplicationModel).filter_by(organisation_id=org_id).all()

    def get_by_id(self, app_id: UUID) -> ApplicationModel | None:
        return self.db.query(ApplicationModel).filter_by(id=app_id).first()

    def get_by_ids(self, app_ids: list[UUID]) -> list[ApplicationModel]:
        return (
            self.db.query(ApplicationModel)
            .filter(ApplicationModel.id.in_(app_ids))
            .all()
        )

    def update(
        self, application_id: UUID, data: CreateApplicationRequestModel
    ) -> ApplicationModel:
        app = (
            self.db.query(ApplicationModel)
            .filter(ApplicationModel.id == application_id)
            .first()
        )
        if not app:
            return None

        app.name = data.name
        app.code = data.name.lower().replace(" ", "_")
        app.description = data.description
        self.db.commit()
        self.db.refresh(app)
        return app
