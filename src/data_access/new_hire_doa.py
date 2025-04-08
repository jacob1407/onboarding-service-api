from sqlalchemy.orm import Session
from ..models.new_hire_model import NewHire

def insert_new_hire(db: Session, name: str, email: str, role: str) -> NewHire:
    hire = NewHire(name=name, email=email, role=role)
    db.add(hire)
    db.commit()
    db.refresh(hire)
    return hire


def get_new_hire_by_id(db: Session, hire_id: int) -> NewHire | None:
    return db.query(NewHire).filter(NewHire.id == hire_id).first()
