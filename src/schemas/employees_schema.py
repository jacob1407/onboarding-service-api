from uuid import UUID
from pydantic import BaseModel


class CreateEmployeeRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    organisation_id: UUID
    role_id: UUID


class GetEmployeeResponseModel(CreateEmployeeRequestModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}
