from sqlalchemy.orm import Session
from uuid import UUID
from ..models.employee_onboarding_requests_model import EmployeeOnboardingRequestModel
from ..enums.employee_onboarding_request_status import EmployeeOnboardingRequestStatus


class EmployeeOnboardingRequestDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_onboarding_request(
        self, employee_id: UUID, application_id: UUID, onboarding_id: UUID
    ) -> UUID:
        request = EmployeeOnboardingRequestModel(
            employee_id=employee_id,
            application_id=application_id,
            status=EmployeeOnboardingRequestStatus.requested,
            onboarding_id=onboarding_id,
        )
        self.db.add(request)
        self.db.flush()
        return request.id

    def get_requests_by_user_id(
        self, user_id: UUID
    ) -> list[EmployeeOnboardingRequestModel]:
        return (
            self.db.query(EmployeeOnboardingRequestModel)
            .filter(EmployeeOnboardingRequestModel.employee_id == user_id)
            .all()
        )

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
