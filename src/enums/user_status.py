import enum


class UserStatus(enum.Enum):
    active = "active"
    invited = "invited"
    inactive = "inactive"
    archived = "archived"
