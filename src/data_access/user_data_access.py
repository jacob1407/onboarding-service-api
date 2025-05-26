from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload


from ..enums.user_type import UserType
from ..models.onboarding_model import OnboardingModel
from ..models.role_model import RoleModel
from ..models.user_model import UserModel
from ..schemas.user_schema import CreateUserRequestModel, UpdateUserRequestModel


class UserDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: CreateUserRequestModel, org_id: UUID) -> UserModel:
        new_user = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            password_hash="",
            type=user.type,
            organisation_id=org_id,
        )
        self.db.add(new_user)
        self.db.flush()
        return new_user

    def get_all_users(self, user_type: UserType, org_id: UUID) -> list[UserModel]:
        query = self.db.query(UserModel)
        if user_type:
            query = query.filter(
                UserModel.type == user_type and UserModel.organisation_id == org_id
            )
        return query.all()

    def get_user_by_id(self, user_id: UUID) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_users_by_user_ids(self, user_ids: list[UUID]) -> list[UserModel]:
        return self.db.query(UserModel).filter(UserModel.id.in_(user_ids)).all()

    def update_user(self, user_id: UUID, data: UpdateUserRequestModel) -> UserModel:
        user = self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.first_name = data.first_name
        user.last_name = data.last_name
        user.email = data.email
        user.username = data.username
        user.type = data.type
        return user

    def get_all_employees_by_org_id(self, org_id: UUID) -> list[UserModel]:
        return (
            self.db.query(UserModel)
            .join(OnboardingModel, OnboardingModel.user_id == UserModel.id)
            .join(RoleModel, RoleModel.id == OnboardingModel.role_id)
            .options(
                joinedload(UserModel.employee_onboarding).joinedload(
                    OnboardingModel.role
                )
            )
            .filter(
                UserModel.type == UserType.employee
                and UserModel.organisation_id == org_id
            )
            .all()
        )

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.username == username).first()
