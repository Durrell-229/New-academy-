from ninja import Router, Schema
from notifications.models import Notification
from typing import List
import uuid

router = Router()

class NotificationOut(Schema):
    id: uuid.UUID
    titre: str
    message: str
    type_alerte: str
    is_read: bool
    created_at: str

    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.isoformat()

@router.get("/", response=List[NotificationOut])
def list_notifications(request):
    return Notification.objects.filter(recipient=request.user)

@router.post("/{notification_id}/read")
def mark_as_read(request, notification_id: uuid.UUID):
    notification = Notification.objects.get(id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return {"success": True}
