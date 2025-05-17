from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..services.auth_service import AuthService

from ..services.users_service import UsersService

from ..schemas.user_schema import CreateUserRequestModel

from ..db.db import get_transactional_session
from ..schemas.auth import Token, TokenData
from ..services.security import create_access_token, verify_password
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
