from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..services.users_service import create_user, get_user
from ..db import get_db
from ..schemas.users_schema import CreateUserRequestModel, GetUserResponseModel

app = APIRouter()


@app.post("/")
def create_user(data: CreateUserRequestModel, db: Session = Depends(get_db)):
    result = create_user(db, data.first_name, data.last_name, data.email, data.role_id)
    return {"message": "New user created", "id": result.id}


@app.get("/{user_id}", response_model=GetUserResponseModel)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
