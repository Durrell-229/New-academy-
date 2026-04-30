from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from exams.models import Exam

def home_view(request):
    return render(request, 'welcome.html', {'is_home': True})

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    pending_exams = Exam.objects.filter(approval_status='pending')

    return render(request, 'admin/dashboard.html', {
        'pending_exams': pending_exams,
        'pending_count': pending_exams.count(),
    })

@login_required
def admin_approve_exam(request, exam_id):
    """Approuve un examen en attente de validation"""
    if not request.user.is_superuser:
        return redirect('home')

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.approval_status = 'approved'
        exam.save()
        messages.success(request, f"Épreuve '{exam.titre}' approuvée avec succès.")

    return redirect('admin_dashboard')

