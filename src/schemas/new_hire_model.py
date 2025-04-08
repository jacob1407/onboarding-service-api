from pydantic import BaseModel


class NewHireIn(BaseModel):
    name: str
    email: str
    role: str

class NewHireOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        orm_mode = True