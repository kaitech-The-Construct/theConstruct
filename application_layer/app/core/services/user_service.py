# core/services/user_service.py

from typing import List
from fastapi import HTTPException, status
from google.cloud import firestore
from schemas.user import UserResponse, UserUpdate


class UserService:
    def __init__(self):
        self.db = firestore.Client()
        self.users_collection = self.db.collection("users")

    def get_user_by_id(self, user_id: str) -> UserResponse:
        user_ref = self.users_collection.document(user_id)
        user = user_ref.get()
        if not user.exists:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponse(**user.to_dict())

    def get_all_users(self) -> List[dict]:
        """Retrieve all users"""
        try:
            user_ref = self.db.collection("users")
            users = [doc.to_dict() for doc in user_ref.stream()]
            return users
        except Exception as exc:
            print(f"Error retrieving user list: {exc}")

    def update_user(self, user_id: str, update_data: UserUpdate) -> UserResponse:
        user_ref = self.users_collection.document(user_id)
        user = user_ref.get()
        if not user.exists:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

        update_data_dict = vars(update_data)

        user_ref.update(update_data_dict)
        return UserResponse(**update_data_dict)

    def delete_user(self, user_id: str) -> None:
        user_ref = self.users_collection.document(user_id)
        user = user_ref.get()
        if not user.exists:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

        user_ref.delete()
