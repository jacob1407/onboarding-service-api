from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..services.organisation_service import OrganisationService
from ..schemas.organisation_schema import CreateOrganisationRequestModel

router = APIRouter()


@router.post("/")
def create_organisation(
    organisation: CreateOrganisationRequestModel, db: Session = Depends(get_db)
):
    service = OrganisationService(db)
    return service.create_organisation(organisation)
