from sqlalchemy.orm import Session
from ..data_access.new_hire_doa import get_new_hire_by_id, insert_new_hire

def create_new_hire(db: Session, name: str, email: str, role: str):
    return insert_new_hire(db, name, email, role)

def get_new_hire(db: Session, hire_id: int):
    return get_new_hire_by_id(db, hire_id)