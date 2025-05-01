import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Literal

from ..enum.user_type import UserType


class CreateUserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    type: UserType
    organisation_id: UUID


class GetUserResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    status: Literal["invited", "active", "inactive", "archived"]
    type: UserType
    organisation_id: UUID

    model_config = {"from_attributes": True}
