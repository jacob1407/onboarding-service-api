from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    String,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..db import Base
from ..enums.user_status import UserStatus
from ..enums.user_type import UserType


class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("username", name="uq_users_username"),
    )

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False, default="")

    organisation_id = Column(
        UUID(as_uuid=True), ForeignKey("organisations.id"), nullable=False
    )

    status = Column(Enum(UserStatus), nullable=False, default=UserStatus.inactive)
    type = Column(Enum(UserType), nullable=False)

    created_date = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_updated_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    employee_profile = relationship(
        "EmployeeProfileModel", uselist=False, back_populates="user"
    )
