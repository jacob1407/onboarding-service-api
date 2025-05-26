from uuid import UUID as PyUUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db.db import Base


class ApplicationContactsModel(Base):
    __tablename__ = "application_contacts"

    application_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("applications.id"),
        primary_key=True,
    )

    contact_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("users.id"),
        primary_key=True,
    )
