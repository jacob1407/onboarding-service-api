import enum
from sqlalchemy import Column, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


class UserStatus(enum.Enum):
    active = "active"
    invited = "invited"
    inactive = "inactive"
    archived = "archived"


class UserStatusModel(Base):
    __tablename__ = "user_status"

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True, nullable=False
    )
    status = Column(Enum(UserStatus), nullable=False)
    last_updated_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("UserModel", back_populates="status")
