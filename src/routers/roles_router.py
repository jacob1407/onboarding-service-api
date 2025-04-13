from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.roles_schema import RoleIn, RoleOut
from ..services.roles_service import add_role, list_roles, fetch_role_by_id
from ..db import get_db  # or wherever you have this defined

app = APIRouter()


@app.post("/", response_model=RoleOut)
def create_role(data: RoleIn, db: Session = Depends(get_db)):
    return add_role(db, data.name, data.display_name)


@app.get("/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db)):
    return list_roles(db)


@app.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: str, db: Session = Depends(get_db)):
    role = fetch_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
