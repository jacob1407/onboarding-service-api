from uuid import UUID
from sqlalchemy.orm import Session

from ..models.employee_model import EmployeeModel
from ..schemas.employees_schema import GetEmployeeResponseModel
from ..data_access.employee_dao import EmployeeDataAccess


class EmployeeService:
    def __init__(self, db: Session):
        self.data_access = EmployeeDataAccess(db)

    def create_employee(
        self, first_name: str, last_name: str, email: str, role_id: UUID
    ):
        return self.data_access.insert_employee(first_name, last_name, email, role_id)

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
