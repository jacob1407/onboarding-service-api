import httpx
from sendgrid.helpers.mail import Mail, Email, To, Content

from ..enums.user_status import UserStatus

from ..schemas.user_schema import GetUserResponseModel

from ..models.user_model import UserModel
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
        contact: UserModel,
        employee: UserModel,
        application: ApplicationModel,
    ):
        subject = (
            f"{employee.first_name} {employee.last_name} needs access to applications"
        )

        body = f"""
        <div style="background-color: #f9f9f9; padding: 20px; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="padding: 20px; border-bottom: 1px solid #eaeaea;">
                    <h2 style="color: #2563eb;">Access Request for Applications</h2>
                </div>
                <div style="padding: 20px;">
                    <p style="color: #333333;">Dear {contact.first_name},</p>

                    <p style="color: #333333;">{employee.first_name} {employee.last_name} has started onboarding and needs access to <strong>{application.name}</strong>.</p>
                    <p>
                        Please log in to Access Manager to review and approve the request.
                    </p>
                    {" " if contact.status == UserStatus.active else "<p style='color: #333333;'>If you haven't activated your account, please do so by following the complete-invitation email sent previously.</p>"}
                </div>
                <div style="padding: 20px; border-top: 1px solid #eaeaea; text-align: center;">
                    <p style="color: #999999; font-size: 12px;">Thanks,<br/>Onboarding Team</p>
                </div>
            </div>
        </div>
        """

        await self._send_email(to=contact.email, subject=subject, html_body=body)

    async def send_invite_email(self, user: GetUserResponseModel, token: str):
        invite_link = f"http://localhost:3000/complete-invite?token={token}"

        subject = "You're invited to join Access Manager"
        html_body = f"""
        <div style="background-color: #f9f9f9; padding: 20px; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <div style="padding: 20px; border-bottom: 1px solid #eaeaea;">
                    <h2 style="color: #2563eb;">You're invited to join Access Manager</h2>
                </div>
                <div style="padding: 20px;">
                    <p style="color: #333333;">Hi {user.first_name},</p>

                    <p style="color: #333333;">You’ve been invited to join Access Manager. Use the following link to activate your account.</p>
                    <p>
                        {invite_link}
                    </p>
                    <p style="color: #333333;">This link will expire in 24 hours.</p>
                </div>
                <div style="padding: 20px; border-top: 1px solid #eaeaea; text-align: center;">
                    <p style="color: #999999; font-size: 12px;">Thanks,<br/>Onboarding Team</p>
                </div>
            </div>
        </div>
        """

        await self._send_email(
            to=user.email,
            subject=subject,
            html_body=html_body,
        )

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
