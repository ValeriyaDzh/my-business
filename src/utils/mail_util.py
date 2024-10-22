import logging
import smtplib
from email.message import EmailMessage

from src.config import settings

logger = logging.getLogger(__name__)


class MailService:

    def __init__(self, email: str, password: str, host: str, port: int) -> None:
        self.email = email
        self.password = password
        self.host = host
        self.port = port

    async def send_verify_email(self, recipient: str, invite_token: int) -> None:

        subject = f"{invite_token} - registration confirmation code on the platform"
        verify_email_template = f"""
                    <div>
                        <h3> Registration</h3>
                        <br>
                        <p>Thank you for registering your company on the MyBusiness corporate platform! 
                        To confirm, enter the code on page</p>
                        <a>
                            {invite_token}
                        </a>
                    </div>
                """
        await self._send(recipient, subject, verify_email_template)

    async def send_invite_email(
        self, recipient: str, password: str, invite_url: str
    ) -> None:

        subject = "Registration on the company"
        invite_email_template = f"""
                    <div>
                        <h3>Registration</h3>
                        <br>
                        <p>Your password to log in to your personal account: {password}</p>
                        <p>To complete registration with the company, please follow the link:</p>
                        <a href="{invite_url}">click</a>
                    </div>
                """
        await self._send(recipient, subject, invite_email_template)

    async def _send(
        self,
        email_to: str,
        subject: str,
        template: str,
        subtype: str = "html",
    ) -> None:
        try:
            with smtplib.SMTP_SSL(self.host, self.port) as server:
                logger.debug("Preparing mail from...")
                server.login(self.email, self.password)
                email = EmailMessage()
                email["Subject"] = subject
                email["From"] = self.email
                email["To"] = email_to

                email.set_content(template, subtype=subtype)
                server.send_message(email)
                logger.debug(f"Mail send to {email_to}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")


mail_service = MailService(
    settings.smtp.EMAIL,
    settings.smtp.PASSWORD.get_secret_value(),
    settings.smtp.HOST,
    settings.smtp.PORT,
)
