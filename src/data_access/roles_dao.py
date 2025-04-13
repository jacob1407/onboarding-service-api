from sqlalchemy.orm import Session
from ..models.role_model import RoleModel


def create_role(db: Session, name: str, display_name: str) -> RoleModel:
    role = RoleModel(name=name, display_name=display_name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_all_roles(db: Session) -> list[RoleModel]:
    return db.query(RoleModel).all()


def get_role_by_id(db: Session, role_id) -> RoleModel | None:
    return db.query(RoleModel).filter(RoleModel.id == role_id).first()
