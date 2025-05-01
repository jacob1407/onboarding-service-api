from sqlalchemy.orm import Session
from ..models.user_model import UserModel
from ..schemas.user_schema import CreateUserRequestModel
import uuid


class UserDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, data: CreateUserRequestModel) -> UserModel:
        user = UserModel(
            id=uuid.uuid4(),
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            username=data.username,
            password_hash="",
            organisation_id=data.organisation_id,
            type=data.type,
            status="inactive",
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_users(self, user_type: str = None) -> list[UserModel]:
        query = self.db.query(UserModel)
        if user_type:
            query = query.filter(UserModel.type == user_type)
        return query.all()

    def get_user_by_id(self, user_id: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def update_user(self, user_id: str, data: CreateUserRequestModel) -> UserModel:
        user = self.get_user_by_id(user_id)
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.email = data.email
        user.username = data.username
        user.type = data.type
        self.db.commit()
        self.db.refresh(user)
        return user
