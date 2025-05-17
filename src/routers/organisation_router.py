from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.db import get_db, get_transactional_session
from ..services.organisation_service import OrganisationService
from ..schemas.organisation_schema import (
    CreateOrganisationRequestModel,
    GetOrganisationResponseModel,
)

router = APIRouter()


@router.post("/")
def create_organisation(
    organisation: CreateOrganisationRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = OrganisationService(db)
    return service.create_organisation(organisation)


@router.get("/{org_id}", response_model=GetOrganisationResponseModel)
def get_organisation(org_id: UUID, db: Session = Depends(get_transactional_session)):
    service = OrganisationService(db)
    org = service.get_organisation_by_id(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organisation not found")
    return org
