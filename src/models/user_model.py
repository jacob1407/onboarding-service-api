import uuid
from datetime import datetime
from uuid import UUID as PyUUID

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    func,
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..models.onboarding_model import OnboardingModel
from ..db.db import Base
from ..enums.user_status import UserStatus
from ..enums.user_type import UserType


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("username", name="uq_users_username"),
    )

    id: Mapped[PyUUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False, default="")

    organisation_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("organisations.id"),
        nullable=False,
    )

    status: Mapped[UserStatus] = mapped_column(
        SAEnum(UserStatus),
        nullable=False,
        default=UserStatus.inactive,
    )

    type: Mapped[UserType] = mapped_column(
        SAEnum(UserType),
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

    employee_onboarding: Mapped["OnboardingModel"] = relationship(
        back_populates="user",
        uselist=False,
        foreign_keys="[OnboardingModel.user_id]",  # still a string reference
    )
