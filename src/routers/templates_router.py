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
    service = TemplateService()
    try:
        return service.create_template(db, template)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[GetTemplateReturnModel])
def list_templates(
    org_id: UUID,
    db: Session = Depends(get_db),
):
    service = TemplateService()
    return service.get_templates_by_org(db, org_id)


@router.put("/{template_id}", response_model=GetTemplateReturnModel)
def update_template(
    template_id: UUID,
    updated_data: CreateTemplateRequestModel,
    db: Session = Depends(get_db),
):
    service = TemplateService()
    return service.update_template(db, template_id, updated_data)


@router.delete("/{template_id}")
def delete_template(
    template_id: UUID,
    db: Session = Depends(get_db),
):
    service = TemplateService()
    service.delete_template(db, template_id)
    return {"detail": "Template deleted successfully."}
