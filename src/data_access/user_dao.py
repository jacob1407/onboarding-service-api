from sqlalchemy.orm import Session
from uuid import UUID
from ..models.user_model import UserModel


def insert_user(
    db: Session, first_name: str, last_name: str, email: str, role_id: UUID
) -> UserModel:
    user = UserModel(
        first_name=first_name, last_name=last_name, email=email, role_id=role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()
