from sqlalchemy.orm import Session
from ..data_access.user_data_access import UserDataAccess
from ..schemas.user_schema import (
    CreateUserRequestModel,
    GetUserResponseModel,
)


class UsersService:
    def __init__(self, db: Session):
        self.__dao = UserDataAccess(db)

    def create_user(self, data: CreateUserRequestModel) -> GetUserResponseModel:
        user = self.__dao.create_user(data)
        return GetUserResponseModel.model_validate(user)

    def get_all_users(self, user_type: str = None) -> list[GetUserResponseModel]:
        users = self.__dao.get_all_users(user_type)
        return [GetUserResponseModel.model_validate(u) for u in users]

    def get_user_by_id(self, user_id: str) -> GetUserResponseModel | None:
        user = self.__dao.get_user_by_id(user_id)
        return GetUserResponseModel.model_validate(user) if user else None

    def update_user(
        self, user_id: str, data: CreateUserRequestModel
    ) -> GetUserResponseModel | None:
        user = self.__dao.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = self.__dao.update_user(user_id, data)
        return GetUserResponseModel.model_validate(updated_user)
