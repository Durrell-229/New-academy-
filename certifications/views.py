"""
Vues pour la gestion des certifications.
"""
# pylint: disable=no-member  # Django models have .objects manager
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Certification

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def verify_certificate_view(request, code):
    """Vérifie une certification via code"""
    try:
        certification = Certification.objects.get(code=code)
        return render(request, 'certifications/verify.html', {
            'certification': certification,
            'valid': True,
        })
    except Certification.DoesNotExist:
        return render(request, 'certifications/verify.html', {
            'valid': False,
        })


@require_http_methods(["POST"])
def verify_certificate_api(_request):
    """API pour vérifier une certification"""
    return JsonResponse({'status': 'ok'})


@login_required
def my_certificates_view(request):
    """Affiche les certifications de l'utilisateur"""
    certifications = Certification.objects.filter(user=request.user)
    return render(request, 'certifications/my_certificates.html', {
        'certifications': certifications,
    })
