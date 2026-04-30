from django.urls import path
from .views import list_compositions, create_composition, composition_detail, submit_composition
from .api import router as compositions_api

urlpatterns = [
    path('', list_compositions, name='list_compositions'),
    path('create/', create_composition, name='create_composition'),
    path('<uuid:composition_id>/', composition_detail, name='composition_detail'),
    path('<uuid:composition_id>/submit/', submit_composition, name='submit_composition'),
]

api_urlpatterns = [
    path('api/v1/compositions/', compositions_api.urls),
]
