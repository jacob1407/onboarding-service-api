from enum import Enum


class EmployeeOnboardingStatus(Enum):
    pending = "pending"
    in_progress = "in_progress"
    complete = "complete"
    cancelled = "cancelled"
