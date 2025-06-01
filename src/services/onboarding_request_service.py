from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.contact_onboarding_request import OnboardingRequestWithEmployeeSchema

from ..data_access.application_contacts_data_access import ApplicationContactDataAccess

from ..data_access.onboarding_data_access import EmployeeOnboardingDataAccess

from ..enums.employee_onboarding_status import EmployeeOnboardingStatus

from ..schemas.onboarding_requests_schema import (
    GetOnboardingRequestResponseModel,
)

from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus
from ..data_access.onboarding_request_data_access import (
    EmployeeOnboardingRequestDataAccess,
)
from ..models.onboarding_requests_model import OnboardingRequestModel


class OnboardingRequestsService:
    def __init__(self, db: Session):
        self.data_access = EmployeeOnboardingRequestDataAccess(db)
        self.onboarding_data_access = EmployeeOnboardingDataAccess(db)
        self.requests_data_access = EmployeeOnboardingRequestDataAccess(db)
        self.app_contacts_data_access = ApplicationContactDataAccess(db)

    def confirm_onboarding_request_complete(
        self, request_id: UUID
    ) -> OnboardingRequestModel | None:
        # Step 1: Get the request
        request = self.data_access.get_request_by_id(request_id)
        if not request:
            return None

        if request.status == EmployeeOnboardingRequestStatus.complete:
            return request

        self.data_access.update_request_status(
            request_id, EmployeeOnboardingRequestStatus.complete
        )

        all_requests = self.data_access.get_requests_by_onboarding_id(
            request.onboarding_id
        )

        if all(
            r.status == EmployeeOnboardingRequestStatus.complete for r in all_requests
        ):
            self.onboarding_data_access.update_onboarding_status(
                request.onboarding_id,
                EmployeeOnboardingStatus.complete,
            )

        return request

    def get_requests_by_user_id(
        self, user_id: UUID
    ) -> list[GetOnboardingRequestResponseModel]:
        requests = self.data_access.get_requests_by_user_id(user_id)

        return [
            GetOnboardingRequestResponseModel(
                id=req.id,
                application_name=req.application.name,
                application_id=req.application.id,
                status=req.status,
                acknowledged_at=req.acknowledged_at,
                completed_at=req.completed_at,
            )
            for req in requests
        ]

    def get_requests_for_contact(
        self, user_id: UUID, status: EmployeeOnboardingRequestStatus
    ) -> list[OnboardingRequestWithEmployeeSchema]:
        app_ids = self.app_contacts_data_access.get_apps_by_contact_id(user_id)

        if not app_ids:
            return []

        app_requests = self.requests_data_access.get_requests_by_application_ids(
            app_ids, status
        )

        return [
            OnboardingRequestWithEmployeeSchema.from_model(req) for req in app_requests
        ]
