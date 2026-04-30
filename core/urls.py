from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

from core.views import home_view, admin_dashboard_view, admin_approve_exam
from core.api_urls import api as core_api
from api.v1.router import api as v1_api

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('admin/exams/<uuid:exam_id>/approve/', admin_approve_exam, name='admin_approve_exam'),

    # Core & Auth URLs
    path('', RedirectView.as_view(url='/showcase/', permanent=False), name='home'), # Redirect root to showcase
    path('dashboard/', home_view, name='dashboard'), # Assuming 'home_view' acts as dashboard for authenticated users
    path('auth/', include('accounts.urls', namespace='accounts')),
    
    # App URLs
    path('showcase/', include('video_showcase.urls')),
    path('exams/', include('exams.urls')),
    path('compositions/', include('compositions.urls')),
    path('correction/', include('correction.urls')),
    path('bulletins/', include('bulletins.urls')),
    path('certificates/', include('certifications.urls')),
    path('qcm/', include('qcm.urls')),
    path('plagiat/', include('plagiat.urls')),
    path('gamification/', include('gamification.urls')), # Include main gamification urls
    path('api/gamification/', include('gamification_api.urls')), # Include gamification API urls
    path('audit/', include('audittrail.urls')),
    path('webhooks/', include('webhooks.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('videoconf/', include('videoconf.urls')),
    path('forums/', include('social.urls')),
    path('calendar/', include('calendar_app.urls')),
    path('documents/', include('documents.urls')),
    path('analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),
    path('cours/', include('cours.urls')),

    # API URLs
    path('api/v1/', v1_api.urls),
    path('api/core/', core_api.urls),
]

# --- Static and Media Files (Development Server) ---
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
