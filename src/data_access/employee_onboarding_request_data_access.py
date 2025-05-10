from sqlalchemy.orm import Session, joinedload
from uuid import UUID

from ..models.employee_onboarding_model import EmployeeOnboardingModel
from ..models.employee_onboarding_requests_model import EmployeeOnboardingRequestModel
from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus


class EmployeeOnboardingRequestDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding_request(
        self, application_id: UUID, onboarding_id: UUID
    ) -> UUID:
        request = EmployeeOnboardingRequestModel(
            application_id=application_id,
            status=EmployeeOnboardingRequestStatus.requested,
            onboarding_id=onboarding_id,
        )
        self.db.add(request)
        self.db.flush()
        return request.id

    def update_request_status(
        self, request_id: UUID, status: EmployeeOnboardingRequestStatus
    ) -> EmployeeOnboardingRequestModel | None:
        request = (
            self.db.query(EmployeeOnboardingRequestModel)
            .filter(EmployeeOnboardingRequestModel.id == request_id)
            .first()
        )

        if request:
            request.status = status
            return request.id

        return None

    def get_requests_by_user_id(
        self, user_id: UUID
    ) -> list[EmployeeOnboardingRequestModel]:
        return (
            self.db.query(EmployeeOnboardingRequestModel)
            .join(
                EmployeeOnboardingModel,
                EmployeeOnboardingModel.id
                == EmployeeOnboardingRequestModel.onboarding_id,
            )
            .filter(EmployeeOnboardingModel.user_id == user_id)
            .options(joinedload(EmployeeOnboardingRequestModel.application))
            .all()
        )
