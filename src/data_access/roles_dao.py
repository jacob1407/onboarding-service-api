from sqlalchemy.orm import Session
from ..models.roles_model import Role


def create_role(db: Session, name: str, display_name: str) -> Role:
    role = Role(name=name, display_name=display_name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_all_roles(db: Session) -> list[Role]:
    return db.query(Role).all()


def get_role_by_id(db: Session, role_id) -> Role | None:
    return db.query(Role).filter(Role.id == role_id).first()
