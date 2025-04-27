from uuid import UUID
from pydantic import BaseModel

from ..schemas.roles_schema import GetRolesResponseModel


class CreateEmployeeRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    organisation_id: UUID
    role_id: UUID


class UpdateEmployeeRequestModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_id: UUID


class GetEmployeesResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    model_config = {"from_attributes": True}


class GetEmployeeResponseModel(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: GetRolesResponseModel

    model_config = {"from_attributes": True}
