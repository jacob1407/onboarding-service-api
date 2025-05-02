from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base
import uuid


class EmployeeOnboardingRequestModel(Base):
    __tablename__ = "employee_onboarding_requests"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    onboarding_id = Column(
        UUID(as_uuid=True), ForeignKey("employee_onboardings.id"), nullable=False
    )
    application_id = Column(
        UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False
    )
    status = Column(String, nullable=False, default="pending")
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
