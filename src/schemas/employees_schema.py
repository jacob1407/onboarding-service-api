from uuid import UUID
from pydantic import BaseModel


class CreateEmployeeRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_id: UUID


class GetEmployeeResponseModel(CreateEmployeeRequestModel):
    id: UUID

    model_config = {"from_attributes": True}
