from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.applications_schema import (
    CreateApplicationRequestModel,
    GetApplicationResponseModel,
    GetApplicationsResponseModel,
)
from ..schemas.auth import TokenData
from ..services.applications_service import ApplicationService
from ..services.security import check_user_auth
from ..db.db import get_transactional_session

router = APIRouter()


@router.post("/", response_model=GetApplicationResponseModel)
def create_application(
    data: CreateApplicationRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = ApplicationService(db)
    return service.create_application(data, auth_data.organisation_id)


@router.get("/", response_model=list[GetApplicationsResponseModel])
def get_applications(
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = ApplicationService(db)
    return service.get_applications_by_org_id(auth_data.organisation_id)


@router.get("/{application_id}", response_model=GetApplicationResponseModel)
def get_application(
    application_id: UUID,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = ApplicationService(db)
    app = service.get_application_by_id(application_id, auth_data.organisation_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app


@router.put("/{application_id}", response_model=GetApplicationResponseModel)
def update_application(
    application_id: UUID,
    data: CreateApplicationRequestModel,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    service = ApplicationService(db)
    updated = service.update_application(
        application_id, data, auth_data.organisation_id
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Application not found")
    return updated


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: UUID, db: Session = Depends(get_transactional_session)
):
    service = ApplicationService(db)
    deleted = service.delete_application(application_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
