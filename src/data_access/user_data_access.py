import uuid
from sqlalchemy.orm import Session, joinedload

from ..enums.user_type import UserType
from ..models.employee_onboarding_model import EmployeeOnboardingModel
from ..models.employee_profile_model import EmployeeProfileModel
from ..models.role_model import RoleModel
from ..models.user_model import UserModel
from ..schemas.user_schema import CreateUserRequestModel


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

    def get_all_employees(self) -> list[UserModel]:
        return (
            self.db.query(UserModel)
            .join(
                EmployeeOnboardingModel, EmployeeOnboardingModel.user_id == UserModel.id
            )
            .join(RoleModel, RoleModel.id == EmployeeOnboardingModel.role_id)
            .options(
                joinedload(UserModel.employee_onboarding).joinedload(
                    EmployeeOnboardingModel.role
                )
            )
            .filter(UserModel.type == UserType.employee)
            .all()
        )
