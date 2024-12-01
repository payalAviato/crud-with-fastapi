from pydantic import BaseModel, EmailStr, Field
from typing import Any, Dict, Optional, List
from datetime import date

class User(BaseModel):
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="Email address of the user")
    project_id: str = Field(..., description="The project this user is associated with")

    mobile_number: Optional[str] = Field(None, description="Mobile phone number of the user")
    company_name: Optional[str] = Field(None, description="Company name (if applicable)")
    dob: Optional[str] = Field(None, description="Date of birth of the user")
    hashtag: Optional[str] = Field(None, description="Hashtag or tag associated with the user")


class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    project_id: Optional[str] = None

    mobile_number: Optional[str] = None
    company_name: Optional[str] = None
    dob: Optional[str] = None
    hashtag: Optional[str] = None


class UserResponse(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    username: str = Field(..., description="Username of the user")
    email: str = Field(..., description="Email address of the user")
    project_id: str = Field(..., description="The project this user is associated with")

    mobile_number: Optional[str] = Field(None, description="Mobile phone number of the user")
    company_name: Optional[str] = Field(None, description="Company name")
    dob: Optional[str] = Field(None, description="Date of birth")
    hashtag: Optional[str] = Field(None, description="Hashtag associated with the user")


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")


class UpdatedUserResponse(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user")
    updated_data: Dict[str, Any] = Field(..., description="Dictionary of updated fields")

class InvitationRequest(BaseModel):
    to_emails: List[EmailStr]  

class InvitationResponse(BaseModel):
    message: str
    recipients: List[EmailStr]