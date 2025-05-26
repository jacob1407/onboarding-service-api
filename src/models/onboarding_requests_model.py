import uuid
from datetime import datetime
from uuid import UUID as PyUUID
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus
from ..db.db import Base

if TYPE_CHECKING:
    from .application_model import ApplicationModel
    from .onboarding_model import OnboardingModel


class OnboardingRequestModel(Base):
    __tablename__ = "employee_onboarding_requests"

    id: Mapped[PyUUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    onboarding_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("employee_onboardings.id"),
        nullable=False,
    )

    application_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("applications.id"),
        nullable=False,
    )

    status: Mapped[EmployeeOnboardingRequestStatus] = mapped_column(
        SAEnum(EmployeeOnboardingRequestStatus),
        nullable=False,
    )

    acknowledged_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    acknowledged_by: Mapped[PyUUID | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    application: Mapped["ApplicationModel"] = relationship(
        back_populates="onboarding_requests"
    )

    onboarding: Mapped["OnboardingModel"] = relationship(back_populates="requests")
