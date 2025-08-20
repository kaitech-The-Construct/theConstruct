# core/services/user_service.py

from typing import List, Optional

from core.config.settings import settings
from google.cloud import firestore
from schemas.user import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self):
        self.db = firestore.Client()
        self.users_collection = self.db.collection(f"{settings.ENVIR}_users")

    def create_user(self, user_data: UserCreate) -> dict:
        """Create User Item"""
        try:
            user_dict = user_data.dict()
            user_dict["profile"] = {}
            user_dict["wallets"] = {}
            user_dict["kyc"] = {"status": "pending"}
            user_dict["is_active"] = True
            user_dict["created_at"] = firestore.SERVER_TIMESTAMP
            doc_ref = self.users_collection.document()
            doc_ref.set(user_dict)
            user_dict["id"] = doc_ref.id
            return user_dict
        except Exception as exc:
            print(f"Error creating user listing: {exc}")

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """Get User by ID"""
        try:
            user_ref = self.users_collection.document(user_id)
            user = user_ref.get()
            if not user.exists:
                return None
            user_dict = user.to_dict()
            user_dict["id"] = user.id
            return user_dict
        except Exception as exc:
            print(f"Error retrieving user by ID: {exc}")

    def get_user_by_email(self, email: str) -> Optional[dict]:
        """Get User by email"""
        try:
            users_ref = self.users_collection.where("email", "==", email).limit(1)
            users = [doc for doc in users_ref.stream()]
            if not users:
                return None
            user_dict = users[0].to_dict()
            user_dict["id"] = users[0].id
            return user_dict
        except Exception as exc:
            print(f"Error retrieving user by email: {exc}")

    def get_all_users(self) -> List[dict]:
        """Retrieve all users"""
        try:
            users = []
            for doc in self.users_collection.stream():
                user_dict = doc.to_dict()
                user_dict["id"] = doc.id
                users.append(user_dict)
            return users
        except Exception as exc:
            print(f"Error retrieving user list: {exc}")

    def update_user(
        self, user_id: str, user_update_data: UserUpdate
    ) -> Optional[dict]:
        """Update User Item"""
        try:
            user_ref = self.users_collection.document(user_id)
            user_data = user_update_data.dict(exclude_unset=True)
            user_ref.update(user_data)
            user = user_ref.get()
            if not user.exists:
                return None
            user_dict = user.to_dict()
            user_dict["id"] = user.id
            return user_dict
        except Exception as exc:
            print(f"Error updating user by ID: {exc}")

    def delete_user(self, user_id: str) -> bool:
        """Delete User Item"""
        try:
            user_ref = self.users_collection.document(user_id)
            user = user_ref.get()
            if not user.exists:
                return False
            user_ref.delete()
            return True
        except Exception as exc:
            print(f"Error deleting user by ID: {exc}")
            return False

    def verify_kyc_documents(self, user_id: str, documents: List[str]) -> bool:
        """Verify KYC documents for a user"""
        try:
            user_ref = self.users_collection.document(user_id)
            kyc_data = {
                "kyc.status": "verified",
                "kyc.documents": documents,
                "kyc.verifiedAt": firestore.SERVER_TIMESTAMP
            }
            user_ref.update(kyc_data)
            return True
        except Exception as exc:
            print(f"Error verifying KYC documents: {exc}")
            return False

    def update_reputation_score(self, user_id: str, transaction_data: dict) -> float:
        """Update user reputation score based on transaction data"""
        try:
            user_ref = self.users_collection.document(user_id)
            user = user_ref.get()
            if not user.exists:
                return 0.0
            
            user_data = user.to_dict()
            reputation = user_data.get("reputation", {"score": 0, "totalTransactions": 0, "successRate": 100})
            
            # Update reputation based on transaction success
            total_transactions = reputation.get("totalTransactions", 0) + 1
            success_rate = reputation.get("successRate", 100)
            
            if transaction_data.get("success", True):
                # Successful transaction improves reputation
                new_score = min(100, reputation.get("score", 0) + 1)
            else:
                # Failed transaction decreases reputation
                new_score = max(0, reputation.get("score", 0) - 2)
                success_rate = ((success_rate * (total_transactions - 1)) + 0) / total_transactions
            
            reputation_update = {
                "reputation.score": new_score,
                "reputation.totalTransactions": total_transactions,
                "reputation.successRate": success_rate
            }
            
            user_ref.update(reputation_update)
            return new_score
        except Exception as exc:
            print(f"Error updating reputation score: {exc}")
            return 0.0

    def get_user_activity_history(self, user_id: str) -> List[dict]:
        """Get user activity history"""
        try:
            # This would typically query a separate activities collection
            activities_ref = self.db.collection(f"{settings.ENVIR}_activities")
            activities = activities_ref.where("userId", "==", user_id).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
            return [{"id": doc.id, **doc.to_dict()} for doc in activities]
        except Exception as exc:
            print(f"Error retrieving user activity history: {exc}")
            return []

    def manage_user_preferences(self, user_id: str, preferences: dict) -> bool:
        """Manage user preferences"""
        try:
            user_ref = self.users_collection.document(user_id)
            preference_update = {f"preferences.{key}": value for key, value in preferences.items()}
            user_ref.update(preference_update)
            return True
        except Exception as exc:
            print(f"Error managing user preferences: {exc}")
            return False
