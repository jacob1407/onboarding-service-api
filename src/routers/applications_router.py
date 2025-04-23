from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from ..schemas.applications_schema import (
    CreateApplicationRequestModel,
    GetApplicationResponseModel,
)
from ..services.applications_service import ApplicationService
from ..db import get_db

router = APIRouter()


@router.post("/", response_model=GetApplicationResponseModel)
def create_application(
    data: CreateApplicationRequestModel, db: Session = Depends(get_db)
):
    service = ApplicationService(db)
    return service.create_application(data)


@router.get("/", response_model=list[GetApplicationResponseModel])
def get_applications(organisation_id: UUID, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    return service.get_applications_by_org_id(organisation_id)


@router.get("/{app_id}", response_model=GetApplicationResponseModel)
def get_application(app_id: UUID, db: Session = Depends(get_db)):
    service = ApplicationService(db)
    app = service.get_application_by_id(app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app
