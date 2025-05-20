from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from ..db.db import Base

if TYPE_CHECKING:
    from .onboarding_requests_model import OnboardingRequestModel
    from .role_model import RoleModel
    from .user_model import UserModel


class OnboardingModel(Base):
    __tablename__ = "employee_onboardings"

    id: Mapped[PyUUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    role_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )
    user_id: Mapped[PyUUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_by: Mapped[PyUUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    status: Mapped[EmployeeOnboardingStatus] = mapped_column(
        SAEnum(EmployeeOnboardingStatus),
        nullable=False,
        default=EmployeeOnboardingStatus.pending,
    )
    started_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    role: Mapped["RoleModel"] = relationship(back_populates="onboardings")
    user: Mapped["UserModel"] = relationship(
        back_populates="employee_onboarding",
        uselist=False,
        foreign_keys=[user_id],
    )
    requests: Mapped[list["OnboardingRequestModel"]] = relationship(
        back_populates="onboarding",
        cascade="all, delete-orphan",
    )
