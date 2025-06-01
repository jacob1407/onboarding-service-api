from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas.onboarding_requests_schema import GetOnboardingRequestResponseModel
from ..services.onboarding_request_service import OnboardingRequestsService

from ..schemas.employee_schema import GetEmployeeResponseModel

from ..services.security import check_admin_user_auth

from ..schemas.auth import TokenData

from ..services.users_service import UsersService
from ..db.db import get_transactional_session
from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    UpdateUserRequestModel,
)


router = APIRouter()


@router.get("/", response_model=list[GetEmployeeResponseModel])
def get_employees(
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.get_all_employees(UUID(auth_data.organisation_id))


@router.post("/", response_model=GetEmployeeResponseModel)
def create_employee(
    data: CreateEmployeeRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_admin_user_auth),
):
    service = UsersService(db)
    return service.create_employee(data, UUID(auth_data.organisation_id))


@router.get(
    "/{user_id}/onboarding-requests",
    response_model=list[GetOnboardingRequestResponseModel],
)
def get_employee_onboarding_requests(
    user_id: UUID, db: Session = Depends(get_transactional_session)
):
    service = OnboardingRequestsService(db)
    return service.get_requests_by_user_id(user_id)


@router.get("/{user_id}", response_model=GetEmployeeResponseModel)
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


@router.put("/{user_id}", response_model=GetEmployeeResponseModel)
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
