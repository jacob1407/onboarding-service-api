import asyncio
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models.application_model import ApplicationModel
from ..models.onboarding_model import OnboardingModel
from ..models.user_model import UserModel

from ..enums.employee_onboarding_status import EmployeeOnboardingStatus

from ..data_access.onboarding_request_data_access import (
    EmployeeOnboardingRequestDataAccess,
)
from ..data_access.onboarding_data_access import EmployeeOnboardingDataAccess
from ..data_access.role_application_data_access import RoleApplicationDataAccess
from ..data_access.application_contacts_data_access import ApplicationContactDataAccess
from ..data_access.user_data_access import UserDataAccess
from ..services.email_service import EmailService


class OnboardingService:
    def __init__(self, db: Session):
        self.employee_onboarding_data_access = EmployeeOnboardingDataAccess(db)
        self.user_data_access = UserDataAccess(db)
        self.role_application_data_access = RoleApplicationDataAccess(db)
        self.application_contacts_data_access = ApplicationContactDataAccess(db)
        self.email_service = EmailService()
        self.onboarding_request_data_access = EmployeeOnboardingRequestDataAccess(db)

    async def start_onboarding(self, user_id: UUID, org_id: UUID) -> UUID:
        employee, onboarding = self._validate_and_get_onboarding(user_id, org_id)

        applications = (
            self.role_application_data_access.get_all_applications_by_role_id(
                onboarding.role_id
            )
        )

        request_email_information = self._prepare_request_email_information(
            applications, onboarding, employee
        )

        await self._send_emails(request_email_information, employee)

        self.employee_onboarding_data_access.update_onboarding_status_by_user_id(
            user_id=user_id,
            status=EmployeeOnboardingStatus.in_progress,
        )

        return onboarding.id

    def _validate_and_get_onboarding(self, user_id: UUID, org_id: UUID):
        employee = self.user_data_access.get_user_by_id(user_id)
        onboarding = self.employee_onboarding_data_access.get_onboarding_by_user_id(
            user_id
        )

        if not employee or not onboarding:
            raise ValueError("User or onboarding record not found")

        if employee.organisation_id != org_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User does not have access to this onboarding process",
            )

        if (
            EmployeeOnboardingStatus(onboarding.status)
            == EmployeeOnboardingStatus.in_progress
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Onboarding process is already in progress.",
            )

        if (
            EmployeeOnboardingStatus(onboarding.status)
            == EmployeeOnboardingStatus.complete
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Onboarding process is already complete.",
            )

        return employee, onboarding

    def _prepare_request_email_information(
        self,
        applications: list[ApplicationModel],
        onboarding: OnboardingModel,
        employee: UserModel,
    ):
        request_email_information = []
        for app in applications:
            contacts = self.application_contacts_data_access.get_all_contacts_by_application_id(
                app.id
            )

            request_id = self.onboarding_request_data_access.create_onboarding_request(
                application_id=app.id,
                onboarding_id=onboarding.id,
            )

            request_email_information.append(
                {
                    "contacts": contacts,
                    "employee": employee,
                    "application": app,
                    "request_id": request_id,
                }
            )

        return request_email_information

    async def _send_emails(
        self, request_email_information: list[dict], employee: UserModel
    ):
        """Send onboarding emails asynchronously."""
        requests = [
            self.email_service.send_application_request_email(
                contact, employee, info["application"], info["request_id"]
            )
            for info in request_email_information
            for contact in info["contacts"]
        ]
        await asyncio.gather(*requests)
