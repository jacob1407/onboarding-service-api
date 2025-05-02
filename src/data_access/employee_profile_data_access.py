from sqlalchemy.orm import Session
from ..models.employee_profile_model import EmployeeProfileModel
import uuid


class EmployeeProfileDataAccess:
    def __init__(self, db: Session):
        self.db = db

    def create_employee_profile(
        self, user_id: uuid.UUID, role_id: uuid.UUID
    ) -> EmployeeProfileModel:
        profile = EmployeeProfileModel(user_id=user_id, role_id=role_id)
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
