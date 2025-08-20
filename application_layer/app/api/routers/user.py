from typing import List

from api.dependencies.auth import get_current_active_user
from core.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserResponse, UserUpdate

router = APIRouter()

user_service = UserService()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """
    Retrieve a specific user by their user ID.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    update_data: UserUpdate,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update user details.
    """
    # Users can only update their own profile
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )
    
    updated_user = user_service.update_user(user_id, update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Delete a user account.
    """
    # Users can only delete their own account
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"ok": True}


@router.post("/{user_id}/kyc")
async def submit_kyc_documents(
    user_id: str,
    documents: List[str],
    current_user: dict = Depends(get_current_active_user)
):
    """
    Submit KYC documents for verification.
    """
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to submit KYC for this user"
        )
    
    success = user_service.verify_kyc_documents(user_id, documents)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to submit KYC documents"
        )
    return {"message": "KYC documents submitted successfully"}


@router.get("/{user_id}/reputation")
async def get_user_reputation(user_id: str):
    """
    Get user reputation score and statistics.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.get("reputation", {"score": 0, "totalTransactions": 0, "successRate": 100})


@router.get("/{user_id}/activity")
async def get_user_activity(
    user_id: str,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get user activity history.
    """
    # Users can only view their own activity
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user's activity"
        )
    
    activities = user_service.get_user_activity_history(user_id)
    return {"activities": activities}


@router.put("/{user_id}/preferences")
async def update_user_preferences(
    user_id: str,
    preferences: dict,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update user preferences.
    """
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update preferences for this user"
        )
    
    success = user_service.manage_user_preferences(user_id, preferences)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user preferences"
        )
    return {"message": "User preferences updated successfully"}
