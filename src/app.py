from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .schemas.new_hire_model import NewHireIn, NewHireOut
from .services.new_hire_service import create_new_hire, get_new_hire

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/new-hire")
def new_hire(data: NewHireIn, db: Session = Depends(get_db)):
    result = create_new_hire(db, data.name, data.email, data.role)
    return {"message": "New hire created", "id": result.id}

@app.get("/new-hire/{hire_id}", response_model=NewHireOut)
def get_hire(hire_id: int, db: Session = Depends(get_db)):
    hire = get_new_hire(db, hire_id)
    if not hire:
        raise HTTPException(status_code=404, detail="New hire not found")
    return hire
