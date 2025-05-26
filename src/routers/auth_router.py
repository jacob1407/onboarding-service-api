from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..services.email_service import EmailService

from ..services.auth_service import AuthService

from ..services.users_service import UsersService

from ..schemas.user_schema import CreateUserRequestModel

from ..db.db import get_transactional_session
from ..schemas.auth import (
    CompleteInviteRequest,
    InviteInfoResponse,
    InviteUserRequest,
    Token,
    TokenData,
)
from ..services.security import (
    check_user_auth,
    create_access_token,
    create_invite_token,
    verify_password,
)
from ..data_access.user_data_access import UserDataAccess  # adjust import to your style

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_transactional_session),
):
    user_data_access = UserDataAccess(db)
    user = user_data_access.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        TokenData(user_id=str(user.id), organisation_id=str(user.organisation_id))
    )
    return {"access_token": token}


@router.post("/register", response_model=Token)
def register(
    user_model: CreateUserRequestModel, db: Session = Depends(get_transactional_session)
):
    auth_service = AuthService(db)
    user_service = UsersService(db)
    existing = user_service.get_user_by_username(user_model.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        user = auth_service.create_user(user_model)
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")

    token = create_access_token(
        TokenData(user_id=str(user.id), organisation_id=str(user.organisation_id))
    )
    return {"access_token": token}


@router.post("/invite")
async def invite_user(
    payload: InviteUserRequest,
    db: Session = Depends(get_transactional_session),
    auth_data: TokenData = Depends(check_user_auth),
):
    user_service = UsersService(db)
    email_service = EmailService()

    existing_user = user_service.get_user_by_username(payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = user_service.create_user_and_set_as_invited(
        CreateUserRequestModel(
            email=payload.email,
            first_name=payload.first_name,
            last_name=payload.last_name,
            username=payload.email,
            password="",
            type=payload.user_type,
        ),
        UUID(auth_data.organisation_id),
    )

    token = create_invite_token(str(new_user.id), auth_data.organisation_id)

    await email_service.send_invite_email(new_user, token)

    return {"message": "Invite sent", "user_id": str(new_user.id)}


@router.get("/invite-info", response_model=InviteInfoResponse)
def get_invite_info(
    token: str,
    db: Session = Depends(get_transactional_session),
):
    user_service = UsersService(db)
    return user_service.get_invite_info(token)


@router.post("/complete-invite")
def complete_invite(
    payload: CompleteInviteRequest,
    db: Session = Depends(get_transactional_session),
):
    user_service = UsersService(db)
    user = user_service.complete_invite(payload)
    return {"message": "User invite completed successfully", "user_id": str(user.id)}
