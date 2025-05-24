from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..services.security import check_user_auth

from ..schemas.auth import TokenData

from ..services.users_service import UsersService
from ..db.db import get_transactional_session
from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    GetEmployeeResponseModel,
    UpdateUserRequestModel,
)


router = APIRouter()


@router.get("/", response_model=list[GetEmployeeResponseModel])
def get_employees(
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = UsersService(db)
    return service.get_all_employees(UUID(auth_data.organisation_id))


@router.post("/", response_model=GetEmployeeResponseModel)
def create_employee(
    data: CreateEmployeeRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = UsersService(db)
    return service.create_employee(data, UUID(auth_data.organisation_id))


@router.get("/{user_id}", response_model=GetEmployeeResponseModel)
def get_employee(user_id: str, db: Session = Depends(get_transactional_session)):
    service = UsersService(db)
    employee = service.get_employee_by_id(UUID(user_id))
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{user_id}", response_model=GetEmployeeResponseModel)
def update_employee(
    user_id: str,
    data: UpdateUserRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = UsersService(db)
    updated = service.update_employee(UUID(user_id), data)
    if not updated:
        raise HTTPException(
            status_code=404, detail="Employee not found or not updatable."
        )
    return updated
