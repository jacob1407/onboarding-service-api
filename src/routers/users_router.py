from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..schemas.employee_schema import GetEmployeeResponseModel


from ..services.email_service import EmailService
from ..enums.user_type import UserType
from ..schemas.auth import (
    TokenData,
)
from ..services.security import (
    check_admin_user_auth,
)
from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    CreateUserRequestModel,
    GetUserResponseModel,
    UpdateUserRequestModel,
)
from ..services.users_service import UsersService
from ..db.db import get_transactional_session

router = APIRouter()


@router.get("/employees", response_model=list[GetEmployeeResponseModel])
def get_employees(
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.get_all_employees(UUID(auth_data.organisation_id))


@router.post("/employees", response_model=GetEmployeeResponseModel)
def create_employee(
    data: CreateEmployeeRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.create_employee(data, UUID(auth_data.organisation_id))


@router.get("/employees/{user_id}", response_model=GetEmployeeResponseModel)
def get_employee(
    user_id: str,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    employee = service.get_employee_by_id(
        UUID(user_id), UUID(auth_data.organisation_id)
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/employees/{user_id}", response_model=GetEmployeeResponseModel)
def update_employee(
    user_id: str,
    data: UpdateUserRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    updated = service.update_employee(
        UUID(user_id), data, UUID(auth_data.organisation_id)
    )
    if not updated:
        raise HTTPException(
            status_code=404, detail="Employee not found or not updatable."
        )
    return updated


@router.post("/", response_model=GetUserResponseModel)
def create_user(
    data: CreateUserRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.create_user(data, UUID(auth_data.organisation_id))


@router.get("/", response_model=list[GetUserResponseModel])
def get_users(
    user_types: list[UserType] | None = Query(default=None),
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.get_all_users(
        user_types=user_types, org_id=UUID(auth_data.organisation_id)
    )


@router.get("/{user_id}", response_model=GetUserResponseModel)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    user = service.get_user_by_id(user_id, UUID(auth_data.organisation_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=GetUserResponseModel)
def update_user(
    user_id: UUID,
    data: UpdateUserRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    updated = service.update_user(user_id, data, UUID(auth_data.organisation_id))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated
