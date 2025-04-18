from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from ..db import get_db
from ..schemas.templates_schema import (
    CreateTemplateRequestModel,
    GetTemplateReturnModel,
)
from ..services.templates_service import TemplateService

router = APIRouter()


@router.post("/", response_model=GetTemplateReturnModel)
def create_template(
    template: CreateTemplateRequestModel,
    db: Session = Depends(get_db),
):
    service = TemplateService(db)
    try:
        return service.create_template(template)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[GetTemplateReturnModel])
def list_templates(
    organisation_id: UUID,
    db: Session = Depends(get_db),
):
    service = TemplateService(db)
    return service.get_templates_by_org(organisation_id)


@router.put("/{template_id}", response_model=GetTemplateReturnModel)
def update_template(
    template_id: UUID,
    updated_data: CreateTemplateRequestModel,
    db: Session = Depends(get_db),
):
    service = TemplateService(db)
    return service.update_template(template_id, updated_data)


@router.delete("/{template_id}")
def delete_template(
    template_id: UUID,
    db: Session = Depends(get_db),
):
    service = TemplateService(db)
    service.delete_template(template_id)
    return {"detail": "Template deleted successfully."}
