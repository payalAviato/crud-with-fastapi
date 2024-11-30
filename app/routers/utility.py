from fastapi import APIRouter, HTTPException
from app.services.email_service import send_email
import os

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates")

def load_template(template_name: str) -> str:
    """Load an HTML template from the templates directory."""
    try:
        with open(os.path.join(TEMPLATES_DIR, template_name), "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading template: {str(e)}")

@router.post("/send_invitation")
async def send_invitation():
    """Send an invitation email using an HTML template."""
    try:
        subject = "API Documentation Invitation"
        to_emails = ["raviyapayal17@gmail.com"]  
        from_email = os.getenv("FROM_EMAIL")  
        api_key = os.getenv("SENDGRID_API_KEY")  

        html_content = load_template("invitation_email.html")

        response = send_email(subject, to_emails, html_content, from_email, api_key)

        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
