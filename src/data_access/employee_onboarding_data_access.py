from sqlalchemy.orm import Session
from ..models.employee_onboarding_model import EmployeeOnboardingModel
from ..enums.employee_onboarding_status import EmployeeOnboardingStatus
from sqlalchemy.dialects.postgresql import UUID


class EmployeeOnboardingDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding(
        self, user_id: UUID, role_id: UUID
    ) -> EmployeeOnboardingModel:
        onboarding = EmployeeOnboardingModel(
            user_id=user_id,
            status=EmployeeOnboardingStatus.pending,
            role_id=role_id,
        )
        self.db.add(onboarding)
        self.db.commit()
        self.db.refresh(onboarding)
        return onboarding

    def get_onboarding_by_user_id(
        self, user_id: UUID
    ) -> EmployeeOnboardingModel | None:
        return (
            self.db.query(EmployeeOnboardingModel)
            .filter(EmployeeOnboardingModel.user_id == user_id)
            .first()
        )

    def update_employee_role(
        self, user_id: UUID, role_id: UUID
    ) -> EmployeeOnboardingModel:
        onboarding = self.get_onboarding_by_user_id(user_id)
        if onboarding is None:
            raise ValueError(f"No onboarding record found for user_id {user_id}")

        onboarding.role_id = role_id
        self.db.commit()
        self.db.refresh(onboarding)
        return onboarding

    def update_onboarding_status_by_user_id(
        self, user_id: UUID, status: EmployeeOnboardingStatus
    ) -> EmployeeOnboardingModel:
        onboarding = self.get_onboarding_by_user_id(user_id)
        if onboarding is None:
            raise ValueError(f"No onboarding record found for user_id {user_id}")

        onboarding.status = status
        self.db.commit()
        self.db.refresh(onboarding)
        return onboarding

    def update_onboarding_status(
        self, onboarding_id: UUID, new_status: EmployeeOnboardingStatus
    ) -> None:
        onboarding = (
            self.db.query(EmployeeOnboardingModel).filter_by(id=onboarding_id).first()
        )
        if onboarding:
            onboarding.status = new_status
