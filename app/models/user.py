from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    project_id: str

class UpdateUser(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    project_id: Optional[str] = None
