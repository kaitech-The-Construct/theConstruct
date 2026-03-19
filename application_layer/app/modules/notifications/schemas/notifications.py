# schemas/notifications.py

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class NotificationType(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"
    IN_APP = "in_app"
    SYSTEM_ALERT = "system_alert"


class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"


class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class EmailNotificationRequest(BaseModel):
    user_id: str = Field(..., description="User ID to send notification to")
    template: str = Field(..., description="Email template name")
    data: Dict[str, Any] = Field(..., description="Template data")
    subject: Optional[str] = Field(None, description="Email subject")
    priority: NotificationPriority = Field(NotificationPriority.MEDIUM, description="Notification priority")


class PushNotificationRequest(BaseModel):
    user_id: str = Field(..., description="User ID to send notification to")
    message: str = Field(..., description="Push notification message")
    title: Optional[str] = Field(None, description="Notification title")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")
    priority: NotificationPriority = Field(NotificationPriority.MEDIUM, description="Notification priority")


class SMSNotificationRequest(BaseModel):
    phone: str = Field(..., description="Phone number to send SMS to")
    message: str = Field(..., description="SMS message")
    priority: NotificationPriority = Field(NotificationPriority.MEDIUM, description="Notification priority")


class SystemAlertRequest(BaseModel):
    alert_type: str = Field(..., description="Type of system alert")
    data: Dict[str, Any] = Field(..., description="Alert data")
    severity: NotificationPriority = Field(NotificationPriority.MEDIUM, description="Alert severity")
    affected_users: Optional[List[str]] = Field(None, description="List of affected user IDs")


class NotificationPreferences(BaseModel):
    user_id: str = Field(..., description="User ID")
    email_enabled: bool = Field(True, description="Enable email notifications")
    push_enabled: bool = Field(True, description="Enable push notifications")
    sms_enabled: bool = Field(False, description="Enable SMS notifications")
    marketing_emails: bool = Field(False, description="Enable marketing emails")
    order_updates: bool = Field(True, description="Enable order update notifications")
    security_alerts: bool = Field(True, description="Enable security alert notifications")


class NotificationRecord(BaseModel):
    id: str = Field(..., description="Notification ID")
    user_id: Optional[str] = Field(None, description="User ID")
    type: NotificationType = Field(..., description="Notification type")
    status: NotificationStatus = Field(..., description="Notification status")
    priority: NotificationPriority = Field(..., description="Notification priority")
    subject: Optional[str] = Field(None, description="Notification subject")
    message: str = Field(..., description="Notification message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")
    created_at: datetime = Field(..., description="Creation timestamp")
    sent_at: Optional[datetime] = Field(None, description="Sent timestamp")
    delivered_at: Optional[datetime] = Field(None, description="Delivered timestamp")
    read_at: Optional[datetime] = Field(None, description="Read timestamp")


class NotificationResponse(BaseModel):
    success: bool = Field(..., description="Success status")
    message: str = Field(..., description="Response message")
    notification_id: Optional[str] = Field(None, description="Notification ID")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional response data")


class NotificationHistory(BaseModel):
    notifications: List[NotificationRecord] = Field(..., description="List of notifications")
    total_count: int = Field(..., description="Total number of notifications")
    unread_count: int = Field(..., description="Number of unread notifications")
