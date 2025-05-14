from sqlalchemy import Column, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus
from ..db import Base
import uuid


class OnboardingRequestModel(Base):
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
    status = Column(
        Enum(EmployeeOnboardingRequestStatus), nullable=False, default="pending"
    )
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(
        UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=True
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)

    application = relationship("ApplicationModel", back_populates="onboarding_requests")
    onboarding = relationship("OnboardingModel", back_populates="requests")
