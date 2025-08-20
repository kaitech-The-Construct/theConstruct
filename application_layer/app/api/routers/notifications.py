# api/routers/notifications.py

from typing import List
from fastapi import APIRouter, HTTPException, status, Query
from core.services.notification_service import NotificationService
from schemas.notifications import (
    EmailNotificationRequest, PushNotificationRequest, SMSNotificationRequest,
    SystemAlertRequest, NotificationPreferences, NotificationResponse,
    NotificationHistory
)

router = APIRouter()
notification_service = NotificationService()


@router.post("/email", response_model=NotificationResponse)
async def send_email(request: EmailNotificationRequest):
    """
    Send an email notification to a user with template support and priority handling.
    """
    try:
        result = notification_service.send_email_notification(request)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email notification: {str(exc)}",
        )


@router.post("/push", response_model=NotificationResponse)
async def send_push(request: PushNotificationRequest):
    """
    Send a push notification to a user with title, message, and additional data.
    """
    try:
        result = notification_service.send_push_notification(request)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send push notification: {str(exc)}",
        )


@router.post("/sms", response_model=NotificationResponse)
async def send_sms(request: SMSNotificationRequest):
    """
    Send an SMS notification to a phone number.
    """
    try:
        result = notification_service.send_sms_notification(request)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send SMS notification: {str(exc)}",
        )


@router.post("/alerts", response_model=NotificationResponse)
async def create_alert(request: SystemAlertRequest):
    """
    Create a system-wide alert with severity levels and affected user targeting.
    """
    try:
        result = notification_service.create_system_alert(request)
        if not result.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.message
            )
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create system alert: {str(exc)}",
        )


@router.put("/preferences")
async def update_preferences(preferences: NotificationPreferences):
    """
    Update user notification preferences for different types of notifications.
    """
    try:
        success = notification_service.manage_notification_preferences(preferences)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update notification preferences"
            )
        return {"message": "Notification preferences updated successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update preferences: {str(exc)}",
        )


@router.get("/history/{user_id}", response_model=NotificationHistory)
async def get_notification_history(
    user_id: str,
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get notification history for a user including read/unread status.
    """
    try:
        result = notification_service.get_notification_history(user_id, limit)
        return result
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get notification history: {str(exc)}",
        )


@router.put("/read/{notification_id}")
async def mark_as_read(notification_id: str, user_id: str):
    """
    Mark a notification as read for a specific user.
    """
    try:
        success = notification_service.mark_notification_as_read(notification_id, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found or access denied"
            )
        return {"message": "Notification marked as read"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark notification as read: {str(exc)}",
        )


@router.get("/alerts/active")
async def get_active_alerts():
    """
    Get all active system alerts.
    """
    try:
        alerts = notification_service.get_active_alerts()
        return {"active_alerts": alerts}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active alerts: {str(exc)}",
        )


@router.put("/alerts/{alert_id}/dismiss")
async def dismiss_alert(alert_id: str):
    """
    Dismiss a system alert.
    """
    try:
        success = notification_service.dismiss_alert(alert_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alert not found"
            )
        return {"message": "Alert dismissed successfully"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to dismiss alert: {str(exc)}",
        )
