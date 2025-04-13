from uuid import UUID
from pydantic import BaseModel
from typing import Optional, List


class RoleIn(BaseModel):
    name: str
    display_name: str
    template_ids: Optional[List[str]] = None


class RoleOut(RoleIn):
    id: UUID

    class Config:
        orm_mode = True
