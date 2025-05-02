from sqlalchemy.orm import Session
from ..models.employee_onboarding_model import EmployeeOnboardingModel
from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from sqlalchemy.dialects.postgresql import UUID


class EmployeeOnboardingDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding(self, user_id: UUID) -> EmployeeOnboardingModel:
        onboarding = EmployeeOnboardingModel(
            user_id=user_id,
            status=EmployeeOnboardingStatus.pending,
        )
        self.db.add(onboarding)
        self.db.commit()
        self.db.refresh(onboarding)
        return onboarding
