from uuid import UUID
from pydantic import BaseModel
from typing import Literal

from ..schemas.roles_schema import GetRolesResponseModel

from ..enum.user_status import UserStatus

from ..enum.user_type import UserType


class CreateUserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    type: UserType
    organisation_id: UUID


class CreateEmployeeRequestModel(CreateUserRequestModel):
    role_id: UUID


class GetUserResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    username: str
    status: UserStatus
    type: UserType
    organisation_id: UUID

    model_config = {"from_attributes": True}


class GetEmployeeResponseModel(GetUserResponseModel):
    role: GetRolesResponseModel

    model_config = {"from_attributes": True}
