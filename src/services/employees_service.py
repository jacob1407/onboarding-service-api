from uuid import UUID
from sqlalchemy.orm import Session

from ..services.roles_service import RolesService

from ..data_access.role_data_access import RoleDataAccess

from ..models.employee_model import EmployeeModel
from ..schemas.employees_schema import (
    CreateEmployeeRequestModel,
    GetEmployeeResponseModel,
    GetEmployeesResponseModel,
    UpdateEmployeeRequestModel,
)
from ..data_access.employee_data_access import EmployeeDataAccess


class EmployeeService:
    def __init__(self, db: Session):
        self.data_access = EmployeeDataAccess(db)
        self.role_service = RolesService(db)

    def create_employee(self, employee: CreateEmployeeRequestModel):
        employee_model = EmployeeModel(
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            role_id=employee.role_id,
            organisation_id=employee.organisation_id,
        )
        return self.data_access.insert_employee(employee_model)

    def get_employee(self, user_id: UUID) -> GetEmployeeResponseModel | None:
        employee = self.data_access.get_employee_by_id(user_id)
        role = self.role_service.get_role_details_by_id(employee.role_id)
        return GetEmployeeResponseModel(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            role=role,
        )

    def get_employees_by_org_id(self, org_id: UUID) -> list[GetEmployeesResponseModel]:
        return self._convert_employees_to_schema(
            self.data_access.get_employees_by_org_id(org_id)
        )

    def _convert_employees_to_schema(
        self,
        employees: list[EmployeeModel],
    ) -> list[GetEmployeesResponseModel]:
        return [GetEmployeesResponseModel.model_validate(emp) for emp in employees]

    def update_employee(
        self, employee_id: UUID, data: UpdateEmployeeRequestModel
    ) -> GetEmployeeResponseModel | None:
        employee = self.data_access.update(employee_id, data)
        if not employee:
            return None

        role = self.role_service.get_role_by_id(data.role_id)

        return GetEmployeeResponseModel(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            role=role,
        )
