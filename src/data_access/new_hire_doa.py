from sqlalchemy.orm import Session
from uuid import UUID
from ..models.new_hire_model import NewHire


def insert_new_hire(
    db: Session, first_name: str, last_name: str, email: str, role_id: UUID
) -> NewHire:
    hire = NewHire(
        first_name=first_name, last_name=last_name, email=email, role_id=role_id
    )
    db.add(hire)
    db.commit()
    db.refresh(hire)
    return hire


def get_new_hire_by_id(db: Session, hire_id: int) -> NewHire | None:
    return db.query(NewHire).filter(NewHire.id == hire_id).first()
