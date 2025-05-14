from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.roles_schema import (
    CreateRoleRequestModel,
    GetRoleResponseModel,
    GetRolesResponseModel,
)
from ..services.roles_service import RolesService
from ..db import get_transactional_session

router = APIRouter()


@router.post("/", response_model=GetRolesResponseModel)
def create_role(
    data: CreateRoleRequestModel, db: Session = Depends(get_transactional_session)
):
    service = RolesService(db)
    return service.create_role(data)


@router.get("/", response_model=list[GetRolesResponseModel])
def get_roles(organisation_id: str, db: Session = Depends(get_transactional_session)):
    service = RolesService(db)
    return service.get_all_roles_by_org_id(organisation_id)


@router.get("/{role_id}", response_model=GetRoleResponseModel)
def get_role(role_id: str, db: Session = Depends(get_transactional_session)):
    service = RolesService(db)
    role = service.get_role_details_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=GetRoleResponseModel)
def update_role(
    role_id: str,
    data: CreateRoleRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = RolesService(db)
    updated = service.update_role(role_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated
