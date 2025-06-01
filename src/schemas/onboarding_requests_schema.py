from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus


class GetOnboardingRequestResponseModel(BaseModel):
    id: UUID
    application_name: str
    application_id: UUID
    status: EmployeeOnboardingRequestStatus
    acknowledged_at: datetime | None
    completed_at: datetime | None
