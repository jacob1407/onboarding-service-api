from uuid import UUID

from pydantic import BaseModel

from ..models.onboarding_requests_model import OnboardingRequestModel


class OnboardingRequestWithEmployeeSchema(BaseModel):
    request_id: UUID
    application_name: str
    employee_name: str
    employee_email: str
    employee_id: UUID
    status: str
    role_id: UUID
    role_name: str

    @classmethod
    def from_model(cls, model: OnboardingRequestModel):
        return cls(
            request_id=model.id,
            application_name=model.application.name,
            employee_name=f"{model.onboarding.user.first_name} {model.onboarding.user.last_name}",
            employee_email=model.onboarding.user.email,
            employee_id=model.onboarding.user.id,
            status=model.status.value,
            role_id=model.onboarding.role_id,
            role_name=model.onboarding.role.name,
        )
