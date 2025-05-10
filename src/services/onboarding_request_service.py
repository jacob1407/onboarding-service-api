from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.onboarding_requests_schema import (
    GetOnboardingRequestResponseModel,
)

from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus
from ..data_access.employee_onboarding_request_data_access import (
    EmployeeOnboardingRequestDataAccess,
)
from ..models.employee_onboarding_requests_model import EmployeeOnboardingRequestModel


class OnboardingRequestsService:
    def __init__(self, db: Session):
        self.data_access = EmployeeOnboardingRequestDataAccess(db)

    def confirm_onboarding_request_complete(
        self, request_id: UUID
    ) -> EmployeeOnboardingRequestModel | None:
        return self.data_access.update_request_status(
            request_id, EmployeeOnboardingRequestStatus.complete
        )

    def get_requests_by_user_id(
        self, user_id: UUID
    ) -> list[GetOnboardingRequestResponseModel]:
        requests = self.data_access.get_requests_by_user_id(user_id)

        return [
            GetOnboardingRequestResponseModel(
                id=req.id,
                application_name=req.application.name,
                application_description=req.application.description,
                application_id=req.application.id,
                status=req.status,
                acknowledged_at=req.acknowledged_at,
                completed_at=req.completed_at,
            )
            for req in requests
        ]
