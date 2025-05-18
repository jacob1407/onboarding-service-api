from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from ..db.db import get_transactional_session

from ..enums.user_type import UserType

from ..data_access.user_data_access import UserDataAccess
from ..schemas.auth import TokenData

# Secret key and algorithm
SECRET_KEY = "b6gGfbOkANbDfjchsMNJSBx5spYGhJO3ii63Yw09M-NLyuUTNaadx-Ba35engczQpwsp4GfzF_udnMoUBtuI3g"  # replace with environment variable later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: TokenData, expires_delta: timedelta = None) -> str:
    to_encode = data.model_dump()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_current_user(
    token: str = Depends(oauth2_scheme), db=Depends(get_transactional_session)
):
    user_data_access = UserDataAccess(db)
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("user_id")
        organisation_id: str = payload.get("organisation_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_data_access.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {"user": user, "org_id": organisation_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def check_user_auth(
    token: str = Depends(oauth2_scheme), db=Depends(get_transactional_session)
):
    user_data_access = UserDataAccess(db)
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("user_id")
        organisation_id: str = payload.get("organisation_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_data_access.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        if user.type not in [
            UserType.admin,
        ]:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not authorized for this action",
            )
        return TokenData(user_id=user_id, organisation_id=organisation_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
