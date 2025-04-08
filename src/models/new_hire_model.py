from sqlalchemy import Column, Integer, String
from ..db import Base

class NewHire(Base):
    __tablename__ = "new_hires"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)