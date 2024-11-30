from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.user import User, UpdateUser, UserResponse, UpdatedUserResponse, ErrorResponse
from app.config.firebase import db
import uuid

router = APIRouter()

@router.post("/", response_model=UserResponse, responses={500: {"model": ErrorResponse}})
async def add_user(user: User):
    """Create a new user."""
    try:
        user_id = str(uuid.uuid4())  
        user_ref = db.collection("users").document(user_id)
        user_ref.set(user.dict())  
        return {"user_id": user_id, **user.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.get("/", response_model=list[UserResponse], responses={500: {"model": ErrorResponse}})
async def get_users():
    """Retrieve all users."""
    try:
        users = []
        users_ref = db.collection("users")
        for doc in users_ref.stream():
            user = doc.to_dict()
            user["user_id"] = doc.id  
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def get_user(user_id: str):
    """Retrieve a single user by their ID."""
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": user_id, **user_doc.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")


@router.patch("/{user_id}", response_model=UpdatedUserResponse, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def update_user(user_id: str, user_data: UpdateUser):
    """Update user details."""
    try:
        user_ref = db.collection("users").document(user_id)
        if not user_ref.get().exists:
            raise HTTPException(status_code=404, detail="User not found")
        user_ref.update(user_data.dict(exclude_unset=True))
        updated_user = user_ref.get()
        return {"user_id": user_id, "updated_data": updated_user.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


@router.delete("/{user_id}", response_model=dict, responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def delete_user(user_id: str):
    """Delete a user."""
    try:
        user_ref = db.collection("users").document(user_id)
        if not user_ref.get().exists:
            raise HTTPException(status_code=404, detail="User not found")
        user_ref.delete()
        return {"message": f"User with ID {user_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
