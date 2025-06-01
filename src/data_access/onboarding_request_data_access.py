from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from ..models.onboarding_model import OnboardingModel
from ..models.onboarding_requests_model import OnboardingRequestModel
from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus


class EmployeeOnboardingRequestDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding_request(
        self, application_id: UUID, onboarding_id: UUID
    ) -> UUID:
        request = OnboardingRequestModel(
            application_id=application_id,
            status=EmployeeOnboardingRequestStatus.requested,
            onboarding_id=onboarding_id,
        )
        self.db.add(request)
        self.db.flush()
        return request.id

    def update_request_status(
        self, request_id: UUID, status: EmployeeOnboardingRequestStatus
    ) -> OnboardingRequestModel | None:
        request = (
            self.db.query(OnboardingRequestModel)
            .filter(OnboardingRequestModel.id == request_id)
            .first()
        )

        if request:
            request.status = status
            return request

        return None

    def get_requests_by_user_id(self, user_id: UUID) -> list[OnboardingRequestModel]:
        return (
            self.db.query(OnboardingRequestModel)
            .join(
                OnboardingModel,
                OnboardingModel.id == OnboardingRequestModel.onboarding_id,
            )
            .filter(OnboardingModel.user_id == user_id)
            .options(joinedload(OnboardingRequestModel.application))
            .all()
        )

    def get_request_by_id(self, request_id: UUID) -> OnboardingRequestModel | None:
        return self.db.query(OnboardingRequestModel).filter_by(id=request_id).first()

    def get_requests_by_onboarding_id(
        self, onboarding_id: UUID
    ) -> list[OnboardingRequestModel]:
        return (
            self.db.query(OnboardingRequestModel)
            .filter_by(onboarding_id=onboarding_id)
            .all()
        )

    def get_requests_by_application_ids(
        self, app_ids: list[UUID], status: EmployeeOnboardingRequestStatus
    ):
        return (
            self.db.query(OnboardingRequestModel)
            .filter(
                OnboardingRequestModel.application_id.in_(app_ids),
                OnboardingRequestModel.status == status,
            )
            .options(
                joinedload(OnboardingRequestModel.application),
                joinedload(OnboardingRequestModel.onboarding).joinedload(
                    OnboardingModel.user
                ),
            )
            .all()
        )
