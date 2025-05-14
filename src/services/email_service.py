from uuid import UUID
import httpx
from sendgrid.helpers.mail import Mail, Email, To, Content

from ..models.user_model import UserModel
from ..models.contact_model import ContactModel
from ..models.application_model import ApplicationModel

SENDGRID_API_KEY = (
    "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"
)


class EmailService:
    def __init__(self):
        self.api_key = SENDGRID_API_KEY
        self.sender = "jacob1998.kim@gmail.com"
        self.base_url = "https://api.sendgrid.com/v3/mail/send"

    async def send_application_request_email(
        self,
        contact: ContactModel,
        employee: UserModel,
        application: ApplicationModel,
        request_id: UUID,
    ):
        subject = (
            f"{employee.first_name} {employee.last_name} needs access to applications"
        )

        body = f"""
        <p>Dear {contact.first_name},</p>

        <p>{employee.first_name} {employee.last_name} has started onboarding and needs access to <strong>{application.name}</strong>.</p>
        <p>
            <a href="http://localhost:8080/onboarding/requests/{request_id}/confirm"
                style="display: inline-block; padding: 10px 16px; background-color: #2563eb; color: white;
                        text-decoration: none; border-radius: 4px; font-weight: bold;">
                Confirm Access Granted
            </a>
        </p>

        <p>Thanks,</p>
        <p>Onboarding Team</p>
        """

        await self._send_email(to=contact.email, subject=subject, html_body=body)

    async def _send_email(self, to: str, subject: str, html_body: str):
        # Build the message using SendGrid helpers
        message = Mail(
            from_email=Email(self.sender),
            to_emails=To(to),
            subject=subject,
            html_content=Content("text/html", html_body),
        )

        payload = message.get()  # Convert Mail object to raw dict

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
            except httpx.HTTPError as exc:
                print(f"SendGrid email send failed: {exc}")
