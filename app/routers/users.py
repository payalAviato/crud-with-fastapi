from fastapi import APIRouter, HTTPException
from app.models.user import User, UpdateUser
from app.config.firebase import db
import uuid

# Create the APIRouter instance
router = APIRouter()

# Add a user
@router.post("/")
async def add_user(user: User):
    """Create a new user."""
    try:
        user_id = str(uuid.uuid4())  # Generate a unique user ID
        user_ref = db.collection("users").document(user_id)
        user_ref.set(user.dict())  # Save user details in Firestore
        return {"user_id": user_id, **user.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


# Get all users
@router.get("/")
async def get_users():
    """Retrieve all users."""
    try:
        users = []
        users_ref = db.collection("users")
        for doc in users_ref.stream():
            user = doc.to_dict()
            user["user_id"] = doc.id  # Include user ID in the response
            users.append(user)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")


# Get a single user by ID
@router.get("/{user_id}")
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


# Update a user
@router.patch("/{user_id}")
async def update_user(user_id: str, user_data: UpdateUser):
    """Update user details."""
    try:
        user_ref = db.collection("users").document(user_id)
        if not user_ref.get().exists:
            raise HTTPException(status_code=404, detail="User not found")
        # Update only the provided fields
        user_ref.update(user_data.dict(exclude_unset=True))
        updated_user = user_ref.get()
        return {"user_id": user_id, "updated_data": updated_user.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


# Delete a user
@router.delete("/{user_id}")
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
