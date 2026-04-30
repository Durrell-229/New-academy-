from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from .models import Notification

@login_required
def list_notifications_view(request):
    """Affiche les notifications de l'utilisateur connecté."""
    
    user = request.user
    # Récupérer les notifications globales ET celles spécifiques à l'utilisateur
    notifications = Notification.objects.filter(
        models.Q(recipient=user) | models.Q(recipient=None)
    ).order_by('-created_at')
    
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)

@login_required
def mark_as_read_view(request, notification_id):
    """Marque une notification spécifique comme lue (via AJAX)."""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Vérifier si la notification appartient à l'utilisateur ou est globale
        if notification.recipient == request.user or notification.recipient is None:
            notification.is_read = True
            notification.save()
            return JsonResponse({'success': True, 'message': 'Notification marquée comme lue.'})
        else:
            return JsonResponse({'success': False, 'error': 'Notification non trouvée ou non autorisée.'}, status=403)
            
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification introuvable.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def create_global_notification_view(request):
    """Page pour créer une notification globale (visible par tous)."""
    if request.user.role != 'admin':
        return redirect('dashboard') # Ou une page d'erreur appropriée
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        message = request.POST.get('message')
        type_alerte = request.POST.get('type_alerte', 'INFO')
        
        if not titre or not message:
            from django.contrib import messages
            messages.error(request, "Le titre et le message sont requis.")
            return redirect('create_global_notification') # Retourner à la page pour corriger

        Notification.objects.create(
            titre=titre,
            message=message,
            type_alerte=type_alerte,
            recipient=None, # Notification globale
        )
        from django.contrib import messages
        messages.success(request, "Notification globale créée avec succès.")
        return redirect('dashboard') # Rediriger vers le dashboard admin

    return render(request, 'notifications/admin_create_notification.html', {
        'notification_types': Notification.TYPES,
    })

