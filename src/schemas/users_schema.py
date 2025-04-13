from uuid import UUID
from pydantic import BaseModel


class CreateUserRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_id: UUID


class GetUserResponseModel(CreateUserRequestModel):
    id: UUID

    class Config:
        orm_mode = True
