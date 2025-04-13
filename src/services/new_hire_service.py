from uuid import UUID
from sqlalchemy.orm import Session
from ..data_access.new_hire_doa import get_new_hire_by_id, insert_new_hire


def create_new_hire(
    db: Session, first_name: str, last_name: str, email: str, role_id: UUID
):
    return insert_new_hire(db, first_name, last_name, email, role_id)


def get_new_hire(db: Session, hire_id: int):
    return get_new_hire_by_id(db, hire_id)
