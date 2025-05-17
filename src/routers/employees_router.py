from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from ..services.users_service import UsersService
from ..db.db import get_transactional_session
from ..schemas.user_schema import CreateEmployeeRequestModel, GetEmployeeResponseModel


router = APIRouter()


@router.get("/", response_model=list[GetEmployeeResponseModel])
def get_employees(db: Session = Depends(get_transactional_session)):
    service = UsersService(db)
    return service.get_all_employees()


@router.post("/", response_model=GetEmployeeResponseModel)
def create_employee(
    data: CreateEmployeeRequestModel, db: Session = Depends(get_transactional_session)
):
    service = UsersService(db)
    return service.create_employee(data)


@router.get("/{user_id}", response_model=GetEmployeeResponseModel)
def get_employee(user_id: str, db: Session = Depends(get_transactional_session)):
    service = UsersService(db)
    employee = service.get_employee_by_id(user_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{user_id}", response_model=GetEmployeeResponseModel)
def update_employee(
    user_id: str,
    data: CreateEmployeeRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = UsersService(db)
    updated = service.update_employee(user_id, data)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Employee not found or not updatable."
        )
    return updated
