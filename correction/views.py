from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CorrectionCopie
from exams.models import Exam, ExamFile
from ai_engine.orchestrator import SmartOrchestrator
import base64

@login_required
def upload_submission(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST' and request.FILES.get('image'):
        submission = CorrectionCopie.objects.create(
            exam=exam,
            student=request.user,
            image=request.FILES['image'],
            status='corrected' # Automatique
        )
        
        # 1. Orchestration IA automatique
        orchestrator = SmartOrchestrator()
        with open(submission.image.path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 2. Récupérer le corrigé type depuis les fichiers de l'examen
        corrige_file = exam.files.filter(type_fichier='corrige_type').first()
        corrige_text = "Corrigé standard"
        if corrige_file:
            try:
                with open(corrige_file.fichier.path, 'r', encoding='utf-8', errors='ignore') as f:
                    corrige_text = f.read()
            except Exception:
                corrige_text = "Corrigé standard"
        
        # 3. Correction IA autonome
        exam_info = {
            'titre': exam.titre,
            'matiere': getattr(exam, 'matiere', 'Inconnue'),
            'classe': getattr(exam, 'classe', 'Inconnue'),
            'note_maximale': float(exam.note_maximale or 20)
        }
        feedback_data = orchestrator.correct_copy(base64_image, corrige_text, exam_info=exam_info, is_image=True)
        
        # Extraction intelligente de la note et de l'appréciation
        if isinstance(feedback_data, dict):
            submission.note_ia = feedback_data.get('note', 0)
            submission.feedback = feedback_data.get('appreciation', '')
            submission.json_resultat = feedback_data
            submission.corrected_text = feedback_data.get('appreciation', '')
        else:
            submission.corrected_text = str(feedback_data)
            
        submission.save()
        
        messages.success(request, "Copie traitée par IA avec succès.")
        return redirect('upload_submission', exam_id=exam.id)
    return render(request, 'correction/upload.html', {'exam': exam})

from django.http import HttpResponse
from bulletins.services import BulletinService
from django.core.files.base import ContentFile

@login_required
def prof_pending_validations_view(request):
    """Liste toutes les copies corrigées par l'IA en attente de validation humaine."""
    if request.user.role not in ['professeur', 'admin']:
        return redirect('dashboard')
    
    if request.user.role == 'admin':
        submissions = CorrectionCopie.objects.filter(status='corrected')
    else:
        submissions = CorrectionCopie.objects.filter(
            status='corrected',
            exam__createur=request.user
        )
        
    return render(request, 'correction/pending_validations.html', {
        'submissions': submissions.select_related('student', 'exam'),
        'total': submissions.count()
    })

@login_required
def approve_submission(request, submission_id):
    if not request.user.is_staff:
        messages.error(request, "Accès réservé aux administrateurs.")
        return redirect('home')

    submission = get_object_or_404(CorrectionCopie, id=submission_id)
    submission.status = 'approved'

    # Génération automatique du bulletin PDF
    pdf_content = BulletinService.generate_bulletin_pdf(submission)
    
    # Extraction de la note (simple parsing du feedback IA)
    # Dans une version future, forcez l'IA à renvoyer un JSON
    if submission.corrected_text and "20" in submission.corrected_text:
        # Logique simplifiée pour extraire la note
        submission.grade = 15.0 # Par défaut si non détecté
        
    submission.save()
    
    # Envoyer la réponse pour téléchargement ou notification
    messages.success(request, "Correction approuvée et bulletin généré.")
    return redirect('admin_dashboard')

@login_required
def download_bulletin(request, submission_id):
    submission = get_object_or_404(CorrectionCopie, id=submission_id)
    pdf = BulletinService.generate_bulletin_pdf(submission)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bulletin_{submission.student.last_name}.pdf"'
    return response
