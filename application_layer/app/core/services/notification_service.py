# core/services/notification_service.py

from typing import List, Optional

from core.config.settings import settings
from google.cloud import firestore


class NotificationService:
    def __init__(self):
        self.db = firestore.Client()
        self.notifications_collection = self.db.collection(f"{settings.ENVIR}_notifications")

    def send_email_notification(self, user_id: str, template: str, data: dict) -> bool:
        """Send an email notification to a user"""
        try:
            # In a real implementation, this would integrate with an email service like SendGrid
            print(f"Sending email to {user_id} with template {template} and data {data}")
            
            # Store notification record
            notification_record = {
                "user_id": user_id,
                "type": "email",
                "template": template,
                "data": data,
                "status": "sent",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.notifications_collection.add(notification_record)
            
            return True
        except Exception as exc:
            print(f"Error sending email notification: {exc}")
            return False

    def send_push_notification(self, user_id: str, message: str) -> bool:
        """Send a push notification to a user"""
        try:
            # In a real implementation, this would integrate with a push notification service like FCM
            print(f"Sending push notification to {user_id}: {message}")
            
            # Store notification record
            notification_record = {
                "user_id": user_id,
                "type": "push",
                "message": message,
                "status": "sent",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.notifications_collection.add(notification_record)
            
            return True
        except Exception as exc:
            print(f"Error sending push notification: {exc}")
            return False

    def create_system_alert(self, alert_type: str, data: dict) -> bool:
        """Create a system-wide alert"""
        try:
            # Store alert record
            alert_record = {
                "type": "system_alert",
                "alert_type": alert_type,
                "data": data,
                "status": "active",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_alerts").add(alert_record)
            
            return True
        except Exception as exc:
            print(f"Error creating system alert: {exc}")
            return False
