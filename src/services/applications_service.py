from sqlalchemy.orm import Session

from ..services.contacts_service import ContactService

from ..services.application_contacts_service import ApplicationContactsService
from ..schemas.applications_schema import (
    CreateApplicationRequestModel,
    GetApplicationResponseModel,
    GetApplicationsResponseModel,
)
from ..data_access.applications_dao import ApplicationsDAO
from ..data_access.contacts_dao import ContactDAO
from uuid import UUID


class ApplicationService:
    def __init__(self, db: Session):
        self.dao = ApplicationsDAO(db)
        self.application_contacts_service = ApplicationContactsService(db)
        self.contact_service = ContactService(db)

    def create_application(
        self, data: CreateApplicationRequestModel
    ) -> GetApplicationResponseModel:
        app = self.dao.create(data)
        if data.contact_ids:
            self.application_contacts_service.associate_contacts_to_application(
                app.id, data.contact_ids
            )

        return GetApplicationResponseModel(
            id=app.id,
            name=app.name,
            code=app.code,
            organisation_id=app.organisation_id,
            description=app.description,
            contact_ids=data.contact_ids,
        )

    def get_applications_by_org_id(
        self, org_id: UUID
    ) -> list[GetApplicationsResponseModel]:
        apps = self.dao.get_by_org_id(org_id)
        return [GetApplicationsResponseModel.model_validate(app) for app in apps]

    def get_application_by_id(self, app_id: UUID) -> GetApplicationResponseModel | None:
        app = self.dao.get_by_id(app_id)
        if not app:
            return None

        contacts = self.application_contacts_service.get_contacts_by_application_id(
            app_id
        )

        return GetApplicationResponseModel(
            id=app.id,
            name=app.name,
            code=app.code,
            organisation_id=app.organisation_id,
            description=app.description,
            contacts=contacts,
        )

    def get_applications_by_ids(
        self, app_ids: list[UUID]
    ) -> list[GetApplicationResponseModel]:
        apps = self.dao.get_by_ids(app_ids)
        return [GetApplicationResponseModel.model_validate(app) for app in apps]

    def update_application(
        self, application_id: UUID, data: CreateApplicationRequestModel
    ) -> GetApplicationResponseModel | None:
        app = self.dao.get_by_id(application_id)
        if not app:
            return None

        updated_app = self.dao.update(application_id, data)
        self.application_contacts_service.update_application_contacts(
            application_id, data.contact_ids or []
        )
        contacts = self.contact_service.get_contacts_by_ids(data.contact_ids or [])

        return GetApplicationResponseModel(
            id=updated_app.id,
            name=updated_app.name,
            code=updated_app.code,
            organisation_id=updated_app.organisation_id,
            description=updated_app.description,
            contacts=contacts,
        )
