from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.user_schema import (
    CreateUserRequestModel,
    GetEmployeeResponseModel,
    GetUserResponseModel,
    CreateEmployeeRequestModel,
)
from ..services.users_service import UsersService
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=GetUserResponseModel)
def create_user(data: CreateUserRequestModel, db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.create_user(data)


@router.get("/", response_model=list[GetUserResponseModel])
def get_users(user_type: str = None, db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.get_all_users(user_type=user_type)


@router.get("/employees", response_model=list[GetEmployeeResponseModel])
def get_employees(db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.get_all_employees()


@router.post("/employees", response_model=GetEmployeeResponseModel)
def create_employee(data: CreateEmployeeRequestModel, db: Session = Depends(get_db)):
    service = UsersService(db)
    return service.create_employee(data)


@router.get("/employees/{user_id}", response_model=GetEmployeeResponseModel)
def get_employee(user_id: str, db: Session = Depends(get_db)):
    service = UsersService(db)
    employee = service.get_employee_by_id(user_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/employees/{user_id}", response_model=GetEmployeeResponseModel)
def update_employee(
    user_id: str,
    data: CreateEmployeeRequestModel,
    db: Session = Depends(get_db),
):
    service = UsersService(db)
    updated = service.update_employee(user_id, data)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Employee not found or not updatable."
        )
    return updated


@router.get("/{user_id}", response_model=GetUserResponseModel)
def get_user(user_id: str, db: Session = Depends(get_db)):
    service = UsersService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=GetUserResponseModel)
def update_user(
    user_id: str, data: CreateUserRequestModel, db: Session = Depends(get_db)
):
    service = UsersService(db)
    updated = service.update_user(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
