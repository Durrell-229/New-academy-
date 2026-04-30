from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from gamification.models import Badge, UserBadge
from accounts.models import User
import json

def get_student_badges_api(request, student_id):
    student = get_object_or_404(User, id=student_id)
    user_badges = UserBadge.objects.filter(user=student).select_related('badge')
    data = [{
        'id': str(ub.badge.id),
        'nom': ub.badge.nom,
        'description': ub.badge.description,
        'icone': ub.badge.icone,
        'obtenu_at': ub.obtenu_at.isoformat()
    } for ub in user_badges]
    return JsonResponse({'status': 'success', 'badges': data})

@csrf_exempt
def award_badge_to_student_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            badge_id = data.get('badge_id')
            student = get_object_or_404(User, id=student_id)
            badge = get_object_or_404(Badge, id=badge_id)
            
            user_badge, created = UserBadge.objects.get_or_create(user=student, badge=badge)
            if created:
                badge.atribuer_a_utilisateur(student)
                return JsonResponse({'status': 'success', 'message': f'Badge {badge.nom} attribué.'})
            return JsonResponse({'status': 'already_owned', 'message': 'L\'étudiant possède déjà ce badge.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

def get_available_badges_api(request):
    badges = Badge.objects.filter(est_actif=True)
    data = [{
        'id': str(b.id),
        'nom': b.nom,
        'description': b.description,
        'icone': b.icone,
        'categorie': b.categorie,
        'rarete': b.rarete
    } for b in badges]
    return JsonResponse({'status': 'success', 'badges': data})
