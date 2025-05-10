from enum import Enum


class EmployeeOnboardingRequestStatus(Enum):
    requested = "requested"
    complete = "complete"
    denied = "denied"
