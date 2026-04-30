from django.urls import path
from . import views

urlpatterns = [
    path('student/<uuid:student_id>/badges/', views.get_student_badges_api, name='get_student_badges'),
    path('award-badge/', views.award_badge_to_student_api, name='award_badge_to_student'),
    path('available-badges/', views.get_available_badges_api, name='get_available_badges'),
]
