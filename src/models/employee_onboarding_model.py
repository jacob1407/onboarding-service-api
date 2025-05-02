from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from ..db import Base
import uuid


class EmployeeOnboardingModel(Base):
    __tablename__ = "employee_onboardings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    started_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(EmployeeOnboardingStatus), nullable=False, default="pending")
    started_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_date = Column(DateTime(timezone=True), nullable=True)
