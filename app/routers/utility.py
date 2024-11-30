from fastapi import APIRouter, HTTPException
from app.services.email_service import send_email
import os

# Create the APIRouter instance
router = APIRouter()

# Path to templates directory
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
        # Email details
        subject = "API Documentation Invitation"
        to_emails = ["raviyapayal17@gmail.com"]  # Replace with recipient list or dynamic input
        from_email = os.getenv("FROM_EMAIL")  # Fetch sender email from environment variables
        api_key = os.getenv("SENDGRID_API_KEY")  # Fetch API key from environment variables

        # Load the template
        html_content = load_template("invitation_email.html")

        # Call the email service to send the email
        response = send_email(subject, to_emails, html_content, from_email, api_key)

        # Return success response
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
