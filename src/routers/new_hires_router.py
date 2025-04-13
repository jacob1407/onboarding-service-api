from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from ..services.new_hire_service import create_new_hire, get_new_hire
from ..db import get_db
from ..schemas.new_hire_schema import NewHireIn, NewHireOut

app = APIRouter()


@app.post("/")
def new_hire(data: NewHireIn, db: Session = Depends(get_db)):
    result = create_new_hire(
        db, data.first_name, data.last_name, data.email, data.role_id
    )
    return {"message": "New hire created", "id": result.id}


@app.get("/{hire_id}", response_model=NewHireOut)
def get_hire(hire_id: int, db: Session = Depends(get_db)):
    hire = get_new_hire(db, hire_id)
    if not hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    return hire
