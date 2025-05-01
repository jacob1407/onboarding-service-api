from fastapi import Depends, APIRouter, HTTPException, Query
from uuid import UUID
from sqlalchemy.orm import Session

from ..services.employees_service import EmployeeService
from ..db import get_db
from ..schemas.employees_schema import (
    CreateEmployeeRequestModel,
    GetEmployeeResponseModel,
    GetEmployeesResponseModel,
    UpdateEmployeeRequestModel,
)

router = APIRouter()


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("/")
def create_employee(
    data: CreateEmployeeRequestModel,
    service: EmployeeService = Depends(get_employee_service),
):
    result = service.create_employee(data)
    return result.id


@router.get("/{employee_id}", response_model=GetEmployeeResponseModel)
def get_employee(
    employee_id: UUID, service: EmployeeService = Depends(get_employee_service)
):
    user = service.get_employee(employee_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[GetEmployeesResponseModel])
def get_employees(
    organisation_id: UUID = Query(...),
    service: EmployeeService = Depends(get_employee_service),
):
    return service.get_employees_by_org_id(organisation_id)


@router.put("/{employee_id}", response_model=GetEmployeeResponseModel)
def update_employee(
    employee_id: UUID,
    data: UpdateEmployeeRequestModel,
    service: EmployeeService = Depends(get_employee_service),
):
    updated = service.update_employee(employee_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated
