from sqlalchemy.orm import Session
from ..data_access.organisation_data_access import OrganisationDataAccess
from ..models.organisation_model import OrganisationModel
from ..schemas.organisation_schema import CreateOrganisationRequestModel


class OrganisationService:
    def __init__(self, db: Session):
        self.data_access = OrganisationDataAccess(db)

    def create_organisation(
        self, create_organisation_model: CreateOrganisationRequestModel
    ):
        create_org_db_model = OrganisationModel(
            name=create_organisation_model.name,
            contact_emails=create_organisation_model.contact_emails,
        )
        return self.data_access.create_organisation(create_org_db_model)
