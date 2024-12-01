from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.models.user import InvitationRequest, InvitationResponse
from typing import List
import os
from app.services.email_service import send_email

router = APIRouter()

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates")

def load_template(template_name: str) -> str:
    """Load an HTML template from the templates directory."""
    try:
        with open(os.path.join(TEMPLATES_DIR, template_name), "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading template: {str(e)}")

@router.post("/send_invitation", response_model=InvitationResponse)
async def send_invitation(request: InvitationRequest):
    """
    Send an invitation email using an HTML template.
    Args:
        request: Contains the list of email addresses to send the invitation to.
    Returns:
        A success message with the list of recipients.
    """
    try:
        subject = "API Documentation Invitation"
        from_email = os.getenv("FROM_EMAIL")
        api_key = os.getenv("SENDGRID_API_KEY")

        html_content = load_template("invitation_email.html")

        response = send_email(subject, request.to_emails, html_content, from_email, api_key)

        return InvitationResponse(
            message="Emails sent successfully",
            recipients=request.to_emails
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
