from sqlalchemy.orm import Session
from fastapi import HTTPException, status

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

    def start_onboarding(self, user_id: str) -> None:
        employee = self.user_data_access.get_user_by_id(user_id)
        onboarding = self.employee_onboarding_data_access.get_onboarding_by_user_id(
            user_id
        )

        if onboarding.status == EmployeeOnboardingStatus.in_progress:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Onboarding process is already in progress.",
            )

        if onboarding.status == EmployeeOnboardingStatus.complete:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Onboarding process is already complete.",
            )

        if not employee or not onboarding:
            raise ValueError("User or onboarding record not found")

        applications = (
            self.role_application_data_access.get_all_applications_by_role_id(
                onboarding.role_id
            )
        )

        for app in applications:
            contacts = self.application_contacts_data_access.get_all_contacts_by_application_id(
                app.id
            )

            request_id = self.onboarding_request_data_access.create_onboarding_request(
                application_id=app.id,
                onboarding_id=onboarding.id,
            )

            # Send emails to all contacts associated with the application
            for contact in contacts:
                self.email_service.send_application_request_email(
                    contact, employee, app, request_id
                )

            # Record the onboarding request as requested

        self.employee_onboarding_data_access.update_onboarding_status_by_user_id(
            user_id=user_id,
            status=EmployeeOnboardingStatus.in_progress,
        )

        return onboarding.id
