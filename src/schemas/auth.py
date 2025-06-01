from uuid import UUID
from pydantic import BaseModel

from ..enums.user_type import UserType


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict[
        str, str
    ]  # Contains user details like id, first_name, last_name, email, username, type


class TokenData(BaseModel):
    user_id: str
    organisation_id: str


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class InviteUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    user_type: UserType


class CompleteInviteRequest(BaseModel):
    token: str
    password: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class InviteInfoResponse(BaseModel):
    user_id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
