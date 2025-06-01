from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..db.db import Base

if TYPE_CHECKING:
    from .onboarding_requests_model import OnboardingRequestModel


class ApplicationModel(Base):
    __tablename__ = "applications"

    id: Mapped[PyUUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)

    organisation_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("organisations.id"),
        nullable=False,
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    onboarding_requests: Mapped[list["OnboardingRequestModel"]] = relationship(
        back_populates="application",
        cascade="all, delete-orphan",
    )
