from uuid import UUID
import requests
import resend
from ..models.employee_model import EmployeeModel
from ..models.contact_model import ContactModel
from ..models.application_model import ApplicationModel

RESEND_API_KEY = "re_jWtvDQjv_LE8m71nzXofRZnitBfeUchWq"


class EmailService:
    def __init__(self):
        self.api_key = RESEND_API_KEY
        self.base_url = "https://api.resend.com/emails"
        self.sender = "Onboarding Team <onboarding@resend.dev>"

    def send_application_request_email(
        self,
        contact: ContactModel,
        employee: EmployeeModel,
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

        self._send_email(to=contact.email, subject=subject, html_body=body)

    def _send_email(self, to: str, subject: str, html_body: str):
        params: resend.Emails.SendParams = {
            "from": self.sender,
            "to": [to],
            "subject": subject,
            "html": html_body,
        }
        resend.api_key = self.api_key
        email = resend.Emails.send(params)
        print(email)
