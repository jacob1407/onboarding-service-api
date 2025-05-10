from sqlalchemy.orm import Session
from uuid import UUID

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
