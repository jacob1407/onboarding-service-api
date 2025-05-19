from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..services.contacts_service import ContactService

from ..services.application_contacts_service import ApplicationContactsService
from ..schemas.applications_schema import (
    CreateApplicationRequestModel,
    GetApplicationResponseModel,
    GetApplicationsResponseModel,
)
from ..data_access.application_data_access import ApplicationDataAccess
from ..data_access.application_contacts_data_access import ApplicationContactDataAccess
from ..data_access.role_application_data_access import RoleApplicationDataAccess
from uuid import UUID


class ApplicationService:
    def __init__(self, db: Session):
        self.data_access = ApplicationDataAccess(db)
        self.application_contacts_service = ApplicationContactsService(db)
        self.contact_service = ContactService(db)
        self.application_contacts_data_access = ApplicationContactDataAccess(db)
        self.role_applications_data_access = RoleApplicationDataAccess(db)

    def create_application(
        self, data: CreateApplicationRequestModel, organisation_id: UUID
    ) -> GetApplicationResponseModel:
        app = self.data_access.create(data, organisation_id)
        if data.contact_ids:
            self.application_contacts_service.associate_contacts_to_application(
                app.id, data.contact_ids
            )
        contacts = self.contact_service.get_contacts_by_ids(data.contact_ids or [])
        return GetApplicationResponseModel(
            id=app.id,
            name=app.name,
            code=app.code,
            description=app.description,
            contacts=contacts,
        )

    def get_applications_by_org_id(
        self, org_id: UUID
    ) -> list[GetApplicationsResponseModel]:
        apps = self.data_access.get_by_org_id(org_id)
        return [GetApplicationsResponseModel.model_validate(app) for app in apps]

    def get_application_by_id(
        self, application_id: UUID, auth_organisation_id: str
    ) -> GetApplicationResponseModel | None:
        application = self.data_access.get_by_id(application_id)
        if not application:
            return None

        if str(application.organisation_id) != auth_organisation_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to view this application",
            )
        contacts = self.application_contacts_service.get_contacts_by_application_id(
            application.id
        )

        return GetApplicationResponseModel(
            id=application.id,
            name=application.name,
            code=application.code,
            description=application.description,
            contacts=contacts,
        )

    def get_applications_by_ids(
        self, app_ids: list[UUID]
    ) -> list[GetApplicationResponseModel]:
        apps = self.data_access.get_by_ids(app_ids)
        return [GetApplicationResponseModel.model_validate(app) for app in apps]

    def update_application(
        self,
        application_id: UUID,
        data: CreateApplicationRequestModel,
        auth_organisation_id: str,
    ) -> GetApplicationResponseModel | None:
        application = self.data_access.get_by_id(application_id)
        if not application:
            return None

        if str(application.organisation_id) != auth_organisation_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to update this application",
            )

        updated_application = self.data_access.update(application_id, data)
        return GetApplicationResponseModel.model_validate(updated_application)

    def delete_application(self, application_id: UUID, org_id: UUID) -> bool:
        application = self.data_access.get_by_id(application_id)
        if not application:
            return False
        if str(application.organisation_id) != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to delete this application",
            )
        self.application_contacts_data_access.delete_by_application_id(application_id)
        self.role_applications_data_access.delete_by_application_id(application_id)
        self.data_access.delete(application_id)
        return True
