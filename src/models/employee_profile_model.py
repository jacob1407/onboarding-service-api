from sqlalchemy import UUID, Column, Date, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base


class EmployeeProfileModel(Base):
    __tablename__ = "employee_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    start_date = Column(Date, nullable=True)
