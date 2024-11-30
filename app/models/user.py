from pydantic import BaseModel
from typing import Any, Dict, Optional

class User(BaseModel):
    username: str
    email: str
    project_id: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    project_id: Optional[str] = None

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    project_id:str

class ErrorResponse(BaseModel):
    detail: str

class UpdatedUserResponse(BaseModel):
    user_id: str
    updated_data: Dict[str, Any]