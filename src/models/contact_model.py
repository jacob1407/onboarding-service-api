from datetime import datetime
from uuid import UUID as PyUUID, uuid4

from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from ..db.db import Base


class ContactModel(Base):
    __tablename__ = "contacts"

    id: Mapped[PyUUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True, unique=True)

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
