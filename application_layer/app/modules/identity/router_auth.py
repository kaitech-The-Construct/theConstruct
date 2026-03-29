from datetime import timedelta
import requests

from .dependencies import get_current_active_user
from core.config.settings import settings
from .services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas.user import UserCreate, UserResponse
from firebase_admin import auth

router = APIRouter()
user_service = UserService()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(new_user_data: UserCreate):
    """
    Register a new user account using Firebase Auth.
    """
    # 1. Check if user already exists in Firestore
    existing_user = user_service.get_user_by_email(new_user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )
    
    # 2. Create User in Firebase Auth
    try:
        firebase_user = auth.create_user(
            email=new_user_data.email,
            password=new_user_data.password,
            display_name=new_user_data.username
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Firebase Registration failed: {str(e)}"
        )
    
    # 3. Save User Metadata to Firestore
    # We do not save the password to Firestore
    new_user_data_dict = new_user_data.dict()
    new_user_data_dict.pop("password", None)
    
    new_user = user_service.create_user(UserCreate(**new_user_data_dict, password=""))
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user in database"
        )
    return new_user


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login using Firebase Identity Toolkit REST API.
    """
    api_key = settings.FIREBASE_API_KEY
    if not api_key:
        # Fallback for local testing if API key is not set
        if form_data.username == "test@example.com":
            return {"access_token": "mock_token_for_testing", "token_type": "bearer"}
            
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase API Key is not configured."
        )

    # Use Firebase REST API to sign in with email and password
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": form_data.username,
        "password": form_data.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = response.json()
    return {"access_token": data["idToken"], "token_type": "bearer"}


@router.post("/refresh")
async def refresh_token(current_user: dict = Depends(get_current_active_user)):
    """
    Firebase handles refresh tokens via the client SDK. 
    This endpoint is provided for compatibility but relies on the client re-authenticating or using their refresh token.
    """
    return {"message": "Use Firebase Client SDK to refresh tokens."}


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_active_user)):
    """
    Logout user (client should discard token).
    """
    return {"message": "Successfully logged out"}


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: dict = Depends(get_current_active_user)):
    """
    Get current user profile from Firestore.
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_active_user)
):
    """
    Update current user profile.
    """
    updated_user = user_service.update_user(current_user["id"], profile_data)
    return updated_user
