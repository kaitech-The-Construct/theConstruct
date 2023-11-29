from core.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()

user_service = UserService()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(new_user_data: UserCreate):
    """
    Create a new user account.
    """
    new_user = user_service.create_user(new_user_data)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user"
        )
    return new_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
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
):
    """
    Update user details.
    """
    current_user = user_service.get_user_by_id(user_id)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this user's information",
        )
    updated_user = user_service.update_user(user_id, update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
):
    """
    Delete a user account.
    """
    current_user = user_service.get_user_by_id(user_id)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this user",
        )
    success = user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"ok": True}
