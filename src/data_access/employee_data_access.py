from sqlalchemy.orm import Session
from uuid import UUID

from ..schemas.employees_schema import UpdateEmployeeRequestModel
from ..models.employee_model import EmployeeModel


class EmployeeDataAccess:
    def __init__(self, db: Session):
        self._db = db

    def insert_employee(self, employee: EmployeeModel) -> EmployeeModel:
        self._db.add(employee)
        self._db.commit()
        self._db.refresh(employee)
        return employee

    def get_employee_by_id(self, employee_id: UUID) -> EmployeeModel | None:
        return (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.id == employee_id)
            .first()
        )

    def get_employees_by_org_id(self, org_id: UUID) -> list[EmployeeModel]:
        return (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.organisation_id == org_id)
            .all()
        )

    def update(
        self, employee_id: UUID, data: UpdateEmployeeRequestModel
    ) -> EmployeeModel | None:
        employee = (
            self._db.query(EmployeeModel)
            .filter(EmployeeModel.id == employee_id)
            .first()
        )
        if not employee:
            return None

        employee.first_name = data.first_name
        employee.last_name = data.last_name
        employee.email = data.email
        employee.role_id = data.role_id

        self._db.commit()
        self._db.refresh(employee)
        return employee
