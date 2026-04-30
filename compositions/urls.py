from django.urls import path
from .views import list_compositions, create_composition, composition_detail, submit_paper_view

urlpatterns = [
    path('', list_compositions, name='list_compositions'),
    path('create/', create_composition, name='create_composition'),
    path('<uuid:composition_id>/', composition_detail, name='composition_detail'),
    path('<uuid:composition_id>/submit/', submit_paper_view, name='submit_composition'),
]
