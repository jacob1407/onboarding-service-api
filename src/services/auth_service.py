import uuid
from sqlalchemy.orm import Session

from ..data_access.user_data_access import UserDataAccess
from .security import hash_password
from ..models.user_model import UserModel
from ..schemas.user_schema import CreateUserRequestModel


class AuthService:
    def __init__(self, db: Session):
        self.user_data_access = UserDataAccess(db)

    def create_user(self, data: CreateUserRequestModel) -> UserModel:
        user = UserModel(
            id=uuid.uuid4(),
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            username=data.username,
            password_hash=hash_password(data.password),
            organisation_id=data.organisation_id,
            type=data.type,
            status="active",
        )
        return self.user_data_access.create_user(user)
