from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('my-notifications/', views.list_notifications_view, name='list_notifications'),
    path('mark-as-read/<uuid:notification_id>/', views.mark_as_read_view, name='mark_as_read'),
    path('admin/create-global/', views.create_global_notification_view, name='create_global_notification'),
]
