from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.orm import Session

from ..services.onboarding_request_service import OnboardingRequestsService

from ..db import get_transactional_session
from ..services.onboarding_service import OnboardingService

router = APIRouter()


class StartOnboardingRequest(BaseModel):
    user_id: UUID


@router.post("/start")
def start_onboarding(
    request: StartOnboardingRequest, db: Session = Depends(get_transactional_session)
):
    try:
        service = OnboardingService(db)
        onboarding_id = service.start_onboarding(user_id=request.user_id)
        return {
            "message": "Onboarding started and emails sent",
            "onboarding_id": onboarding_id,
        }
    except HTTPException as e:
        return {
            "message": e.detail,
            "status_code": e.status_code,
        }


@router.get("/requests/{request_id}/confirm")
def confirm_onboarding_request(
    request_id: UUID, db: Session = Depends(get_transactional_session)
):
    service = OnboardingRequestsService(db)
    updated = service.confirm_onboarding_request_complete(request_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Request not found")
    return (
        "Thank you for confirming the onboarding request. You can close this tab now."
    )
