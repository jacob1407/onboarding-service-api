from uuid import UUID
from pydantic import BaseModel

from ..schemas.roles_schema import GetRolesResponseModel
from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from ..enums.user_status import UserStatus
from ..enums.user_type import UserType


class CreateUserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    type: UserType
    password: str


class CreateEmployeeRequestModel(CreateUserRequestModel):
    first_name: str
    last_name: str
    email: str
    username: str
    type: UserType
    password: str = ""
    role_id: UUID


class GetUserResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    username: str
    status: UserStatus
    type: UserType

    model_config = {"from_attributes": True}


class GetEmployeeResponseModel(GetUserResponseModel):
    role: GetRolesResponseModel
    onboarding_status: EmployeeOnboardingStatus | None = None

    model_config = {"from_attributes": True}


class UpdateUserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    type: UserType
    role_id: UUID


class InviteUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    user_type: UserType
