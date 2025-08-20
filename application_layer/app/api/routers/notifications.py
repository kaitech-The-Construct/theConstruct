# api/routers/notifications.py

from core.services.notification_service import NotificationService
from fastapi import APIRouter, HTTPException, status

router = APIRouter()
notification_service = NotificationService()


@router.post("/email")
async def send_email(notification_data: dict):
    """
    Send an email notification to a user.
    """
    user_id = notification_data.get("user_id")
    template = notification_data.get("template")
    data = notification_data.get("data")
    
    if not all([user_id, template, data]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID, template, and data are required",
        )
    
    success = notification_service.send_email_notification(user_id, template, data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email notification",
        )
    return {"message": "Email notification sent successfully"}


@router.post("/push")
async def send_push(notification_data: dict):
    """
    Send a push notification to a user.
    """
    user_id = notification_data.get("user_id")
    message = notification_data.get("message")
    
    if not all([user_id, message]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and message are required",
        )
    
    success = notification_service.send_push_notification(user_id, message)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send push notification",
        )
    return {"message": "Push notification sent successfully"}


@router.post("/alerts")
async def create_alert(alert_data: dict):
    """
    Create a system-wide alert.
    """
    alert_type = alert_data.get("alert_type")
    data = alert_data.get("data")
    
    if not all([alert_type, data]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alert type and data are required",
        )
    
    success = notification_service.create_system_alert(alert_type, data)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create system alert",
        )
    return {"message": "System alert created successfully"}
