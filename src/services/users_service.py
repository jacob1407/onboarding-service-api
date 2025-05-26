from tokenize import Token
from uuid import UUID
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from ..data_access.role_data_access import RoleDataAccess
from ..schemas.roles_schema import GetRolesResponseModel

from ..schemas.employee_schema import GetEmployeeResponseModel
from ..enums.user_status import UserStatus
from ..schemas.auth import CompleteInviteRequest, InviteInfoResponse
from ..services.security import create_access_token, decode_access_token, hash_password
from ..models.user_model import UserModel
from ..data_access.onboarding_data_access import EmployeeOnboardingDataAccess
from ..data_access.user_data_access import UserDataAccess
from ..enums.user_type import UserType

from ..schemas.user_schema import (
    CreateEmployeeRequestModel,
    CreateUserRequestModel,
    GetUserResponseModel,
    UpdateUserRequestModel,
)


class UsersService:
    def __init__(self, db: Session):
        self.__data_access = UserDataAccess(db)
        self.__roles_service = RoleDataAccess(db)
        self.__onboarding_data_access = EmployeeOnboardingDataAccess(db)

    def create_user(
        self, data: CreateUserRequestModel, org_id: UUID
    ) -> GetUserResponseModel:
        user = self.__data_access.create_user(data, org_id)
        return GetUserResponseModel.model_validate(user)

    def create_user_and_set_as_invited(
        self, data: CreateUserRequestModel, org_id: UUID
    ) -> GetUserResponseModel:
        user = self.__data_access.create_user(data, org_id)
        user.status = UserStatus.invited
        return GetUserResponseModel.model_validate(user)

    def get_all_users(
        self, user_type: UserType, org_id: UUID
    ) -> list[GetUserResponseModel]:
        users = self.__data_access.get_all_users(user_type, org_id)
        return [GetUserResponseModel.model_validate(u) for u in users]

    def get_user_by_id(
        self, user_id: UUID, org_id: UUID
    ) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if user and user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to view this user",
            )
        return GetUserResponseModel.model_validate(user) if user else None

    def get_user_model_by_id(self, user_id: UUID, org_id: UUID) -> UserModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if user and user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to view this user",
            )
        return user if user else None

    def get_users_by_ids(self, user_ids: list[UUID]) -> list[GetUserResponseModel]:
        users = self.__data_access.get_users_by_user_ids(user_ids)
        return [GetUserResponseModel.model_validate(u) for u in users]

    def get_user_by_username(self, username: str) -> UserModel | None:
        return self.__data_access.get_user_by_username(username)

    def update_user(
        self, user_id: UUID, data: UpdateUserRequestModel, org_id: UUID
    ) -> GetUserResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user:
            return None
        if user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to update this user",
            )
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
        if not role:
            raise HTTPException(status_code=404, detail="User role not found")

        return GetEmployeeResponseModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            type=user.type,
            role=GetRolesResponseModel.model_validate(role),
        )

    def get_employee_by_id(
        self, user_id: UUID, org_id: UUID
    ) -> GetEmployeeResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user or user.type != UserType.employee:
            return None
        if user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to view this employee",
            )

        onboarding = self.__onboarding_data_access.get_onboarding_by_user_id(user_id)
        if not onboarding:
            return None
        role = self.__roles_service.get_role_by_id(onboarding.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="User role not found")

        return GetEmployeeResponseModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
            status=user.status,
            type=user.type,
            role=GetRolesResponseModel.model_validate(role),
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
        self, user_id: UUID, data: UpdateUserRequestModel, org_id: UUID
    ) -> GetEmployeeResponseModel | None:
        user = self.__data_access.get_user_by_id(user_id)
        if not user or user.type != UserType.employee:
            return None
        if user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to update this employee",
            )
        updated_user = self.__data_access.update_user(user_id, data)
        updated_onboarding = self.__onboarding_data_access.update_employee_role(
            user_id, data.role_id
        )

        role = self.__roles_service.get_role_by_id(data.role_id)
        if not role:
            raise HTTPException(status_code=404, detail="User role not found")

        return GetEmployeeResponseModel.model_validate(
            {
                **updated_user.__dict__,
                "role": GetRolesResponseModel.model_validate(role),
                "onboarding_status": updated_onboarding.status,
            }
        )

    def complete_invite(self, payload: CompleteInviteRequest) -> GetUserResponseModel:
        try:
            payload_data = decode_access_token(payload.token)
            if payload_data.get("purpose") != "invite":
                raise HTTPException(status_code=400, detail="Invalid invite token")
            user_id = UUID(payload_data["user_id"])
            org_id = UUID(payload_data["org_id"])
        except (JWTError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = self.__data_access.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.status != UserStatus.invited:
            raise HTTPException(status_code=400, detail="User not in invited status")
        if user.organisation_id != org_id:
            raise HTTPException(
                status_code=401,
                detail="User does not have access to complete this invite",
            )
        if payload.password == "":
            raise HTTPException(status_code=400, detail="Password cannot be empty")

        user.password_hash = hash_password(payload.password)
        if payload.username:
            user.username = payload.username
        if payload.first_name:
            user.first_name = payload.first_name
        if payload.last_name:
            user.last_name = payload.last_name
        user.status = UserStatus.active

        return GetUserResponseModel.model_validate(user)

    def get_invite_info(self, token: str) -> InviteInfoResponse:
        try:
            payload = decode_access_token(token)
            if payload.get("purpose") != "invite":
                raise HTTPException(status_code=400, detail="Invalid invite token")
            user_id = UUID(payload["user_id"])
            org_id = UUID(payload["org_id"])
        except (JWTError, ValueError):
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = self.get_user_by_id(user_id, org_id)

        if not user or user.status != UserStatus.invited:
            raise HTTPException(
                status_code=404, detail="Invite not found or already accepted"
            )

        return InviteInfoResponse(
            user_id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
