from sqlalchemy.orm import Session

from ..db.db import get_db

from ..models.organisation_model import OrganisationModel


class OrganisationDataAccess:
    def __init__(self, db: Session):
        self._db = db

    def create_organisation(self, organisation_model: OrganisationModel):
        self._db.add(organisation_model)
        self._db.flush()
        return organisation_model
