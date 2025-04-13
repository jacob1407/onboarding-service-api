from uuid import UUID
from sqlalchemy.orm import Session
from ..data_access.user_dao import get_user_by_id, insert_user


def create_user(
    db: Session, first_name: str, last_name: str, email: str, role_id: UUID
):
    return insert_user(db, first_name, last_name, email, role_id)


def get_user(db: Session, user_id: int):
    return get_user_by_id(db, user_id)
