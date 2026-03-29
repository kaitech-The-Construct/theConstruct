from typing import Optional

from core.security import get_current_user as verify_firebase_token
from .services.user_service import UserService
from fastapi import Depends, HTTPException, status

user_service = UserService()

async def get_current_user(token_payload: dict = Depends(verify_firebase_token)):
    """
    Dependency to get the current authenticated user from Firestore using Firebase token payload.
    """
    email = token_payload.get("email")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_service.get_user_by_email(email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """
    Dependency to get the current active user
    """
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
