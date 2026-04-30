import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class MeetingRoom(models.Model):
    STATUS_CHOICES = [
        ('scheduled', _('Planifiée')),
        ('live', _('En direct')),
        ('ended', _('Terminée')),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(_('Nom de la salle'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    google_meet_link = models.CharField(_('Lien Google Meet'), max_length=500, blank=True)
    access_code = models.CharField(_("Code d'accès"), max_length=20, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_public = models.BooleanField(_('Publique'), default=True)
    max_participants = models.IntegerField(_('Participants max'), default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(_('Débutée le'), blank=True, null=True)
    ended_at = models.DateTimeField(_('Terminée le'), blank=True, null=True)
    status = models.CharField(_('Statut'), max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_rooms', 
        verbose_name=_('Créateur')
    )

    class Meta:
        verbose_name = _('Salle de réunion')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def participant_count(self):
        return self.participants.filter(status='in_room').count()


class RoomParticipant(models.Model):
    ROLE_CHOICES = [
        ('host', _('Hôte')),
        ('moderator', _('Modérateur')),
        ('participant', _('Participant')),
    ]

    PARTICIPANT_STATUS = [
        ('waiting', _("Salle d'attente")),
        ('in_room', _('Dans la salle')),
        ('left', _('A quitté')),
    ]

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='participants', verbose_name=_('Salle'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_participations', verbose_name=_('Utilisateur'))
    role = models.CharField(_('Rôle'), max_length=20, choices=ROLE_CHOICES, default='participant')
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(_('A quitté le'), blank=True, null=True)
    is_muted = models.BooleanField(_('Muet'), default=False)
    is_camera_on = models.BooleanField(_('Caméra active'), default=True)
    status = models.CharField(_('Statut'), max_length=20, choices=PARTICIPANT_STATUS, default='in_room')

    class Meta:
        verbose_name = _('Participant')
        ordering = ['joined_at']
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user} in {self.room}"


class RoomMessage(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Salle'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_messages', verbose_name=_('Utilisateur'))
    content = models.TextField(_('Message'))
    created_at = models.DateTimeField(auto_now_add=True)
    is_system_message = models.BooleanField(_('Message système'), default=False)

    class Meta:
        verbose_name = _('Message de salle')
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user}: {self.content[:50]}"
