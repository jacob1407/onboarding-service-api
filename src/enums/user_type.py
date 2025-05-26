import enum


class UserType(enum.Enum):
    admin = "admin"
    access_manager = "access_manager"
    employee = "employee"
