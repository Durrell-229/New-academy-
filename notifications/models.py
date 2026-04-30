import uuid
from django.db import models
from django.conf import settings

class Notification(models.Model):
    TYPES = [
        ('INFO', 'Information'),
        ('SUCCESS', 'Succès'),
        ('WARNING', 'Alerte'),
        ('URGENT', 'Urgent'),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        null=True, 
        blank=True
    )
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_alerte = models.CharField(max_length=10, choices=TYPES, default='INFO')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} - {self.recipient}"
