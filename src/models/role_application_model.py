from uuid import UUID as PyUUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..db.db import Base


class RoleApplicationModel(Base):
    __tablename__ = "role_applications"

    role_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )

    application_id: Mapped[PyUUID] = mapped_column(
        ForeignKey("applications.id"),
        primary_key=True,
    )
