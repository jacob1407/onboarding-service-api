from uuid import UUID
from sqlalchemy.orm import Session

from ..models.employee_model import EmployeeModel
from ..schemas.employees_schema import (
    CreateEmployeeRequestModel,
    GetEmployeeResponseModel,
)
from ..data_access.employee_dao import EmployeeDataAccess


class EmployeeService:
    def __init__(self, db: Session):
        self.data_access = EmployeeDataAccess(db)

    def create_employee(self, employee: CreateEmployeeRequestModel):
        employee_model = EmployeeModel(
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            role_id=employee.role_id,
            organisation_id=employee.organisation_id,
        )
        return self.data_access.insert_employee(employee_model)

    def get_employee(self, user_id: int):
        return self.data_access.get_employee_by_id(user_id)

    def get_employees_by_org_id(self, org_id: UUID) -> list[GetEmployeeResponseModel]:
        return self._convert_employees_to_schema(
            self.data_access.get_employees_by_org_id(org_id)
        )

    def _convert_employees_to_schema(
        self,
        employees: list[EmployeeModel],
    ) -> list[GetEmployeeResponseModel]:
        return [GetEmployeeResponseModel.model_validate(emp) for emp in employees]
