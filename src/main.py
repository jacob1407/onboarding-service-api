from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NewHire(BaseModel):
    name: str
    email: str
    role: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/new-hire")
def create_new_hire(hire: NewHire):
    # In the future, trigger access workflows here
    return {
        "message": "New hire created",
        "data": hire.dict()
    }
