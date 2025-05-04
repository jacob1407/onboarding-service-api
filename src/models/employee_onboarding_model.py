import uuid
from sqlalchemy import Column, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from ..db import Base


class EmployeeOnboardingModel(Base):
    __tablename__ = "employee_onboardings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        nullable=False,
        server_default="0d4941ae-f6ca-44fa-8b53-6588ee97e904",
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    started_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(Enum(EmployeeOnboardingStatus), nullable=False, default="pending")
    started_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_date = Column(DateTime(timezone=True), nullable=True)

    role = relationship("RoleModel", back_populates="onboardings")
    user = relationship(
        "UserModel",
        back_populates="employee_onboarding",
        uselist=False,
        foreign_keys=[user_id],
    )
