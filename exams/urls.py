from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list_view, name='exam_list'),
    path('create/', views.exam_create_view, name='exam_create'),
    path('manage/', views.prof_exams_manage_view, name='prof_exams_manage'),
    path('admin/entities/', views.admin_entities_manage_view, name='admin_entities_manage'),
    path('<str:exam_id>/', views.exam_detail_view, name='exam_detail'),
]
