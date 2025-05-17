from sqlalchemy.orm import Session, joinedload


from ..enums.user_type import UserType
from ..models.onboarding_model import OnboardingModel
from ..models.role_model import RoleModel
from ..models.user_model import UserModel
from ..schemas.user_schema import CreateUserRequestModel


class UserDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.flush()
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
        return user

    def get_all_employees(self) -> list[UserModel]:
        return (
            self.db.query(UserModel)
            .join(OnboardingModel, OnboardingModel.user_id == UserModel.id)
            .join(RoleModel, RoleModel.id == OnboardingModel.role_id)
            .options(
                joinedload(UserModel.employee_onboarding).joinedload(
                    OnboardingModel.role
                )
            )
            .filter(UserModel.type == UserType.employee)
            .all()
        )

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.username == username).first()
