from sqlalchemy.orm import Session
from ..models.onboarding_model import OnboardingModel
from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from uuid import UUID


class EmployeeOnboardingDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding(self, user_id: UUID, role_id: UUID) -> OnboardingModel:
        onboarding = OnboardingModel(
            user_id=user_id,
            status=EmployeeOnboardingStatus.pending,
            role_id=role_id,
        )
        self.db.add(onboarding)
        self.db.flush()
        return onboarding

    def get_onboarding_by_user_id(self, user_id: UUID) -> OnboardingModel | None:
        return self.db.query(OnboardingModel).filter_by(user_id=user_id).first()

    def update_employee_role(self, user_id: UUID, role_id: UUID) -> OnboardingModel:
        onboarding = self.get_onboarding_by_user_id(user_id)
        if onboarding is None:
            raise ValueError(f"No onboarding record found for user_id {user_id}")

        onboarding.role_id = role_id
        return onboarding

    def update_onboarding_status_by_user_id(
        self, user_id: UUID, status: EmployeeOnboardingStatus
    ) -> OnboardingModel:
        onboarding = self.get_onboarding_by_user_id(user_id)
        if onboarding is None:
            raise ValueError(f"No onboarding record found for user_id {user_id}")

        onboarding.status = status
        return onboarding

    def update_onboarding_status(
        self, onboarding_id: UUID, new_status: EmployeeOnboardingStatus
    ) -> None:
        onboarding = (
            self.db.query(OnboardingModel)
            .filter(OnboardingModel.id == onboarding_id)
            .first()
        )
        if onboarding:
            onboarding.status = new_status
