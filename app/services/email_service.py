from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import HTTPException

def send_email(subject: str, to_emails: list, html_content: str, from_email: str, api_key: str):
    """Send an email using SendGrid."""
    try:
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            html_content=html_content
        )
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        # Check if the email was sent successfully
        if response.status_code in [200, 202]:
            return {"message": "Email sent successfully!"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
