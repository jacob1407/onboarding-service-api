from fastapi import Depends, APIRouter, HTTPException, Query
from uuid import UUID
from sqlalchemy.orm import Session

from ..services.employees_service import EmployeeService
from ..db import get_db
from ..schemas.employees_schema import (
    CreateEmployeeRequestModel,
    GetEmployeeResponseModel,
)

router = APIRouter()


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("/")
def create_employee(
    data: CreateEmployeeRequestModel,
    service: EmployeeService = Depends(get_employee_service),
):
    result = service.create_employee(
        data.first_name, data.last_name, data.email, data.role_id
    )
    return {"message": "New user created", "id": result.id}


@router.get("/{user_id}", response_model=GetEmployeeResponseModel)
def get_employee(
    user_id: int, service: EmployeeService = Depends(get_employee_service)
):
    user = service.get_employee(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[GetEmployeeResponseModel])
def get_employees(
    org_id: UUID = Query(...), service: EmployeeService = Depends(get_employee_service)
):
    return service.get_employees_by_org_id(org_id)
