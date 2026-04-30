from django.urls import path
from . import views, views_supervision

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('supervision/', views_supervision.supervision_view, name='supervision'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('admin/users/', views.admin_users_list_view, name='admin_users_list'),
    path('admin/users/<uuid:user_id>/toggle/', views.admin_user_toggle_view, name='admin_user_toggle'),
]
