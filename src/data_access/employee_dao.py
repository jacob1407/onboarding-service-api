from sqlalchemy.orm import Session
from uuid import UUID
from ..models.employee_model import EmployeeModel


class EmployeeDataAccess:
    def __init__(self, db: Session):
        self._db = db

    def insert_employee(
        self, first_name: str, last_name: str, email: str, role_id: UUID
    ) -> EmployeeModel:
        employee = EmployeeModel(
            first_name=first_name, last_name=last_name, email=email, role_id=role_id
        )
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
            self._db.query(EmployeeModel).filter(EmployeeModel.org_id == org_id).all()
        )
