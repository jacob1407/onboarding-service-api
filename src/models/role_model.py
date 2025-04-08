from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from ..db import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    template_ids = Column(JSONB, nullable=True)  # List of UUIDs or strings
