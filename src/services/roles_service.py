from sqlalchemy.orm import Session
from ..data_access.roles_dao import create_role, get_all_roles, get_role_by_id


def add_role(db: Session, name: str, display_name: str):
    return create_role(db, name, display_name)


def list_roles(db: Session):
    return get_all_roles(db)


def fetch_role_by_id(db: Session, role_id):
    return get_role_by_id(db, role_id)
