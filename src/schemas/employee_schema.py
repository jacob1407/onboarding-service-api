from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from .roles_schema import GetRolesResponseModel
from .user_schema import GetUserResponseModel


class GetEmployeeResponseModel(GetUserResponseModel):
    role: GetRolesResponseModel
    onboarding_status: EmployeeOnboardingStatus | None = None

    model_config = {"from_attributes": True}
