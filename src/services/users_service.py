from sqlalchemy.orm import Session

from ..data_access.employee_profile_data_access import EmployeeProfileDataAccess

from ..services.roles_service import RolesService

from ..enum.user_type import UserType
from ..data_access.user_data_access import UserDataAccess
from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    CreateUserRequestModel,
    GetEmployeeResponseModel,
    GetUserResponseModel,
)


class UsersService:
    def __init__(self, db: Session):
        self.__data_access = UserDataAccess(db)
        self.__roles_service = RolesService(db)
        self.__employee_profile_data_access = EmployeeProfileDataAccess(db)

    def create_user(self, data: CreateUserRequestModel) -> GetUserResponseModel:
        user = self.__data_access.create_user(data)
        return GetUserResponseModel.model_validate(user)

    def get_all_users(self, user_type: str = None) -> list[GetUserResponseModel]:
        users = self.__data_access.get_all_users(user_type)
        return [GetUserResponseModel.model_validate(u) for u in users]

    def get_user_by_id(self, user_id: str) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        return GetUserResponseModel.model_validate(user) if user else None

    def update_user(
        self, user_id: str, data: CreateUserRequestModel
    ) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = self.__data_access.update_user(user_id, data)
        return GetUserResponseModel.model_validate(updated_user)

    def create_employee(
        self, data: CreateEmployeeRequestModel
    ) -> GetEmployeeResponseModel:
        if data.type != UserType.employee:
            raise ValueError("User type must be 'employee' to create an employee")

        user = self.__data_access.create_user(data)
        self.__employee_profile_data_access.create_employee_profile(
            user.id, data.role_id
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
            organisation_id=user.organisation_id,
            role=role,
        )

    def get_employee_by_id(self, user_id: str) -> GetEmployeeResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        print(user)
        if not user or user.type != UserType.employee:
            return None

        profile = self.__employee_profile_data_access.get_employee_profile(user_id)
        if not profile:
            return None

        role = self.__roles_service.get_role_by_id(profile.role_id)

        return GetEmployeeResponseModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            type=user.type,
            organisation_id=user.organisation_id,
            role=role,
        )
