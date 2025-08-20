# core/services/notification_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from core.config.settings import settings
from google.cloud import firestore
from schemas.notifications import (
    NotificationType, NotificationStatus, NotificationPriority,
    EmailNotificationRequest, PushNotificationRequest, SMSNotificationRequest,
    SystemAlertRequest, NotificationPreferences, NotificationRecord,
    NotificationResponse, NotificationHistory
)


class NotificationService:
    def __init__(self):
        self.db = firestore.Client()
        self.notifications_collection = self.db.collection(f"{settings.ENVIR}_notifications")
        self.preferences_collection = self.db.collection(f"{settings.ENVIR}_notification_preferences")
        self.alerts_collection = self.db.collection(f"{settings.ENVIR}_alerts")

    def send_email_notification(self, request: EmailNotificationRequest) -> NotificationResponse:
        """Send an email notification to a user"""
        try:
            # Check user preferences
            if not self._check_user_preferences(request.user_id, NotificationType.EMAIL):
                return NotificationResponse(
                    success=False,
                    message="User has disabled email notifications"
                )
            
            notification_id = str(uuid.uuid4())
            
            # In a real implementation, this would integrate with an email service like SendGrid
            print(f"Sending email to {request.user_id} with template {request.template}")
            
            # Store notification record
            notification_record = {
                "id": notification_id,
                "user_id": request.user_id,
                "type": NotificationType.EMAIL.value,
                "template": request.template,
                "subject": request.subject,
                "data": request.data,
                "priority": request.priority.value,
                "status": NotificationStatus.SENT.value,
                "created_at": firestore.SERVER_TIMESTAMP,
                "sent_at": firestore.SERVER_TIMESTAMP
            }
            self.notifications_collection.document(notification_id).set(notification_record)
            
            return NotificationResponse(
                success=True,
                message="Email notification sent successfully",
                notification_id=notification_id
            )
        except Exception as exc:
            print(f"Error sending email notification: {exc}")
            return NotificationResponse(
                success=False,
                message=f"Failed to send email notification: {str(exc)}"
            )

    def send_push_notification(self, request: PushNotificationRequest) -> NotificationResponse:
        """Send a push notification to a user"""
        try:
            # Check user preferences
            if not self._check_user_preferences(request.user_id, NotificationType.PUSH):
                return NotificationResponse(
                    success=False,
                    message="User has disabled push notifications"
                )
            
            notification_id = str(uuid.uuid4())
            
            # In a real implementation, this would integrate with FCM or similar service
            print(f"Sending push notification to {request.user_id}: {request.message}")
            
            # Store notification record
            notification_record = {
                "id": notification_id,
                "user_id": request.user_id,
                "type": NotificationType.PUSH.value,
                "title": request.title,
                "message": request.message,
                "data": request.data,
                "priority": request.priority.value,
                "status": NotificationStatus.SENT.value,
                "created_at": firestore.SERVER_TIMESTAMP,
                "sent_at": firestore.SERVER_TIMESTAMP
            }
            self.notifications_collection.document(notification_id).set(notification_record)
            
            return NotificationResponse(
                success=True,
                message="Push notification sent successfully",
                notification_id=notification_id
            )
        except Exception as exc:
            print(f"Error sending push notification: {exc}")
            return NotificationResponse(
                success=False,
                message=f"Failed to send push notification: {str(exc)}"
            )

    def send_sms_notification(self, request: SMSNotificationRequest) -> NotificationResponse:
        """Send an SMS notification"""
        try:
            notification_id = str(uuid.uuid4())
            
            # In a real implementation, this would integrate with Twilio or similar service
            print(f"Sending SMS to {request.phone}: {request.message}")
            
            # Store notification record
            notification_record = {
                "id": notification_id,
                "phone": request.phone,
                "type": NotificationType.SMS.value,
                "message": request.message,
                "priority": request.priority.value,
                "status": NotificationStatus.SENT.value,
                "created_at": firestore.SERVER_TIMESTAMP,
                "sent_at": firestore.SERVER_TIMESTAMP
            }
            self.notifications_collection.document(notification_id).set(notification_record)
            
            return NotificationResponse(
                success=True,
                message="SMS notification sent successfully",
                notification_id=notification_id
            )
        except Exception as exc:
            print(f"Error sending SMS notification: {exc}")
            return NotificationResponse(
                success=False,
                message=f"Failed to send SMS notification: {str(exc)}"
            )

    def create_system_alert(self, request: SystemAlertRequest) -> NotificationResponse:
        """Create a system-wide alert"""
        try:
            alert_id = str(uuid.uuid4())
            
            # Store alert record
            alert_record = {
                "id": alert_id,
                "type": NotificationType.SYSTEM_ALERT.value,
                "alert_type": request.alert_type,
                "data": request.data,
                "severity": request.severity.value,
                "affected_users": request.affected_users,
                "status": "active",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.alerts_collection.document(alert_id).set(alert_record)
            
            # If specific users are affected, send individual notifications
            if request.affected_users:
                for user_id in request.affected_users:
                    self._send_alert_notification(user_id, request.alert_type, request.data)
            
            return NotificationResponse(
                success=True,
                message="System alert created successfully",
                notification_id=alert_id
            )
        except Exception as exc:
            print(f"Error creating system alert: {exc}")
            return NotificationResponse(
                success=False,
                message=f"Failed to create system alert: {str(exc)}"
            )

    def manage_notification_preferences(self, preferences: NotificationPreferences) -> bool:
        """Manage user notification preferences"""
        try:
            preferences_data = {
                "user_id": preferences.user_id,
                "email_enabled": preferences.email_enabled,
                "push_enabled": preferences.push_enabled,
                "sms_enabled": preferences.sms_enabled,
                "marketing_emails": preferences.marketing_emails,
                "order_updates": preferences.order_updates,
                "security_alerts": preferences.security_alerts,
                "updated_at": firestore.SERVER_TIMESTAMP
            }
            
            self.preferences_collection.document(preferences.user_id).set(preferences_data)
            return True
        except Exception as exc:
            print(f"Error managing notification preferences: {exc}")
            return False

    def get_notification_history(self, user_id: str, limit: int = 50) -> NotificationHistory:
        """Get notification history for a user"""
        try:
            # Query user notifications
            notifications_query = self.notifications_collection.where(
                "user_id", "==", user_id
            ).order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit)
            
            notifications = []
            unread_count = 0
            
            for doc in notifications_query.stream():
                notification_data = doc.to_dict()
                
                # Convert timestamps
                created_at = notification_data.get("created_at")
                if hasattr(created_at, 'timestamp'):
                    created_at = datetime.fromtimestamp(created_at.timestamp())
                
                sent_at = notification_data.get("sent_at")
                if sent_at and hasattr(sent_at, 'timestamp'):
                    sent_at = datetime.fromtimestamp(sent_at.timestamp())
                
                delivered_at = notification_data.get("delivered_at")
                if delivered_at and hasattr(delivered_at, 'timestamp'):
                    delivered_at = datetime.fromtimestamp(delivered_at.timestamp())
                
                read_at = notification_data.get("read_at")
                if read_at and hasattr(read_at, 'timestamp'):
                    read_at = datetime.fromtimestamp(read_at.timestamp())
                
                notification_record = NotificationRecord(
                    id=notification_data.get("id", doc.id),
                    user_id=notification_data.get("user_id"),
                    type=NotificationType(notification_data.get("type")),
                    status=NotificationStatus(notification_data.get("status")),
                    priority=NotificationPriority(notification_data.get("priority", "medium")),
                    subject=notification_data.get("subject"),
                    message=notification_data.get("message", ""),
                    data=notification_data.get("data"),
                    created_at=created_at or datetime.utcnow(),
                    sent_at=sent_at,
                    delivered_at=delivered_at,
                    read_at=read_at
                )
                
                notifications.append(notification_record)
                
                if not read_at:
                    unread_count += 1
            
            return NotificationHistory(
                notifications=notifications,
                total_count=len(notifications),
                unread_count=unread_count
            )
        except Exception as exc:
            print(f"Error getting notification history: {exc}")
            return NotificationHistory(
                notifications=[],
                total_count=0,
                unread_count=0
            )

    def mark_notification_as_read(self, notification_id: str, user_id: str) -> bool:
        """Mark a notification as read"""
        try:
            notification_ref = self.notifications_collection.document(notification_id)
            notification_doc = notification_ref.get()
            
            if not notification_doc.exists:
                return False
            
            notification_data = notification_doc.to_dict()
            if notification_data.get("user_id") != user_id:
                return False
            
            notification_ref.update({
                "status": NotificationStatus.READ.value,
                "read_at": firestore.SERVER_TIMESTAMP
            })
            
            return True
        except Exception as exc:
            print(f"Error marking notification as read: {exc}")
            return False

    def _check_user_preferences(self, user_id: str, notification_type: NotificationType) -> bool:
        """Check if user has enabled this type of notification"""
        try:
            preferences_doc = self.preferences_collection.document(user_id).get()
            
            if not preferences_doc.exists:
                # Default to enabled if no preferences set
                return True
            
            preferences = preferences_doc.to_dict()
            
            if notification_type == NotificationType.EMAIL:
                return preferences.get("email_enabled", True)
            elif notification_type == NotificationType.PUSH:
                return preferences.get("push_enabled", True)
            elif notification_type == NotificationType.SMS:
                return preferences.get("sms_enabled", False)
            
            return True
        except Exception as exc:
            print(f"Error checking user preferences: {exc}")
            return True  # Default to enabled on error

    def _send_alert_notification(self, user_id: str, alert_type: str, data: Dict[str, Any]) -> None:
        """Send individual notification for system alert"""
        try:
            notification_id = str(uuid.uuid4())
            
            notification_record = {
                "id": notification_id,
                "user_id": user_id,
                "type": NotificationType.IN_APP.value,
                "message": f"System Alert: {alert_type}",
                "data": data,
                "priority": NotificationPriority.HIGH.value,
                "status": NotificationStatus.SENT.value,
                "created_at": firestore.SERVER_TIMESTAMP,
                "sent_at": firestore.SERVER_TIMESTAMP
            }
            
            self.notifications_collection.document(notification_id).set(notification_record)
        except Exception as exc:
            print(f"Error sending alert notification: {exc}")

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active system alerts"""
        try:
            alerts_query = self.alerts_collection.where("status", "==", "active")
            
            alerts = []
            for doc in alerts_query.stream():
                alert_data = doc.to_dict()
                alert_data["id"] = doc.id
                alerts.append(alert_data)
            
            return alerts
        except Exception as exc:
            print(f"Error getting active alerts: {exc}")
            return []

    def dismiss_alert(self, alert_id: str) -> bool:
        """Dismiss a system alert"""
        try:
            alert_ref = self.alerts_collection.document(alert_id)
            alert_ref.update({
                "status": "dismissed",
                "dismissed_at": firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as exc:
            print(f"Error dismissing alert: {exc}")
            return False
