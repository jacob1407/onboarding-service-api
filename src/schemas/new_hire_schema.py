from uuid import UUID
from pydantic import BaseModel


class NewHireIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    role_id: UUID


class NewHireOut(NewHireIn):
    id: UUID

    class Config:
        orm_mode = True
