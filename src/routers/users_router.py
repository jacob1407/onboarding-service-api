from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..schemas.auth import Token, TokenData
from ..services.security import create_access_token, verify_password
from ..services.auth_service import AuthService

from ..schemas.user_schema import (
    CreateUserRequestModel,
    GetUserResponseModel,
)
from ..services.users_service import UsersService
from ..db.db import get_transactional_session

router = APIRouter()


@router.post("/", response_model=GetUserResponseModel)
def create_user(
    data: CreateUserRequestModel, db: Session = Depends(get_transactional_session)
):
    service = UsersService(db)
    return service.create_user(data)


@router.get("/", response_model=list[GetUserResponseModel])
def get_users(user_type: str = None, db: Session = Depends(get_transactional_session)):
    service = UsersService(db)
    return service.get_all_users(user_type=user_type)


@router.get("/{user_id}", response_model=GetUserResponseModel)
def get_user(user_id: str, db: Session = Depends(get_transactional_session)):
    service = UsersService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=GetUserResponseModel)
def update_user(
    user_id: str,
    data: CreateUserRequestModel,
    db: Session = Depends(get_transactional_session),
):
    service = UsersService(db)
    updated = service.update_user(user_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_transactional_session),
):
    users_service = UsersService(db)
    user = users_service.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token(
        TokenData(user_id=str(user.id), org_id=str(user.organisation_id))
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
        TokenData(user_id=str(user.id), org_id=str(user.organisation_id))
    )
    return {"access_token": token}
