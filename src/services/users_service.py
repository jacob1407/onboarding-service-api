from uuid import UUID
from sqlalchemy.orm import Session

from ..models.user_model import UserModel

from ..data_access.onboarding_data_access import EmployeeOnboardingDataAccess
from ..services.roles_service import RolesService
from ..data_access.user_data_access import UserDataAccess

from ..enums.user_type import UserType

from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    CreateUserRequestModel,
    GetEmployeeResponseModel,
    GetUserResponseModel,
    UpdateUserRequestModel,
)


class UsersService:
    def __init__(self, db: Session):
        self.__data_access = UserDataAccess(db)
        self.__roles_service = RolesService(db)
        self.__onboarding_data_access = EmployeeOnboardingDataAccess(db)

    def create_user(self, data: CreateUserRequestModel) -> GetUserResponseModel:
        user = self.__data_access.create_user(data)
        return GetUserResponseModel.model_validate(user)

    def get_all_users(
        self, user_type: UserType | None = None
    ) -> list[GetUserResponseModel]:
        users = self.__data_access.get_all_users(user_type)
        return [GetUserResponseModel.model_validate(u) for u in users]

    def get_user_by_id(self, user_id: UUID) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        return GetUserResponseModel.model_validate(user) if user else None

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.__data_access.get_user_by_username(username)

    def update_user(
        self, user_id: UUID, data: UpdateUserRequestModel
    ) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = self.__data_access.update_user(user_id, data)
        return GetUserResponseModel.model_validate(updated_user)

    def create_employee(
        self, data: CreateEmployeeRequestModel, org_id: UUID
    ) -> GetEmployeeResponseModel:
        if data.type != UserType.employee:
            raise ValueError("User type must be 'employee' to create an employee")

        user = self.__data_access.create_user(data, org_id)

        # Create employee onboarding record
        self.__onboarding_data_access.create_onboarding(
            user_id=user.id, role_id=data.role_id
        )
        role = self.__roles_service.get_role_by_id(data.role_id)

        return GetEmployeeResponseModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            type=user.type,
            role=role,
        )

    def get_employee_by_id(self, user_id: UUID) -> GetEmployeeResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user or user.type != UserType.employee:
            return None

        onboarding = self.__onboarding_data_access.get_onboarding_by_user_id(user_id)
        if not onboarding:
            return None
        role = self.__roles_service.get_role_by_id(onboarding.role_id)

        return GetEmployeeResponseModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            type=user.type,
            role=role,
            onboarding_status=onboarding.status if onboarding else None,
        )

    def get_all_employees(self, org_id: UUID) -> list[GetEmployeeResponseModel]:
        records = self.__data_access.get_all_employees_by_org_id(org_id)
        return [
            GetEmployeeResponseModel.model_validate(
                {
                    **record.__dict__,
                    "role": record.employee_onboarding.role,
                    "onboarding_status": record.employee_onboarding.status,
                }
            )
            for record in records
            if record.employee_onboarding
        ]

    def update_employee(
        self, user_id: UUID, data: UpdateUserRequestModel
    ) -> GetEmployeeResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user or user.type != UserType.employee:
            return None

        updated_user = self.__data_access.update_user(user_id, data)
        updated_onboarding = self.__onboarding_data_access.update_employee_role(
            user_id, data.role_id
        )

        role = self.__roles_service.get_role_by_id(data.role_id)

        return GetEmployeeResponseModel.model_validate(
            {
                **updated_user.__dict__,
                "role": role,
                "onboarding_status": updated_onboarding.status,
            }
        )
