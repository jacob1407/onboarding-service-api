from typing import TYPE_CHECKING
import uuid
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


from ..db.db import Base

if TYPE_CHECKING:
    from .onboarding_model import OnboardingModel  # type checker only


class RoleModel(Base):
    __tablename__ = "roles"

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

    onboardings: Mapped[list["OnboardingModel"]] = relationship(back_populates="role")
