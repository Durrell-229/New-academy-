from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import CompositionSession, StudentSubmissionFile, Resultat
from exams.models import Exam, ExamAssignment
from django.contrib import messages

@login_required
def list_compositions(request):
    """Liste les compositions accessibles à l'utilisateur."""
    user = request.user
    
    if user.role == 'eleve':
        # Élèves voient les compositions qui leur sont assignées ou publiques
        compos_assignees = CompositionSession.objects.filter(eleve=user).exclude(statut=CompositionSession.Statut.TERMINEE)
        exam_ids_assignees = compos_assignees.values_list('exam_id', flat=True)
        
        compos_publiques = Exam.objects.filter(est_public=True, statut='publie').exclude(id__in=exam_ids_assignees)
        
        all_compositions = list(compos_assignees.select_related('exam__matiere')) + list(compos_publiques.select_related('matiere'))
        
        return render(request, 'compositions/list_eleve.html', {
            'compositions': all_compositions,
        })
    elif user.role in ['professeur', 'admin']:
        # Professeurs/Admins voient celles qu'ils ont créées ou toutes les publiques
        compos_creees = Exam.objects.filter(createur=user)
        compos_publiques = Exam.objects.filter(est_public=True).exclude(createur=user)
        
        all_compositions = list(compos_creees) + list(compos_publiques)
        
        return render(request, 'compositions/list_prof.html', {
            'compositions': all_compositions,
        })
    else:
        return redirect('dashboard')


@login_required
def create_composition(request):
    """Page pour créer une nouvelle composition (Prof/Admin)."""
    if request.user.role not in ['professeur', 'admin']:
        return redirect('dashboard')

    if request.method == 'POST':
        # Traitement du formulaire de création
        titre = request.POST.get('titre')
        exam_id = request.POST.get('exam_id') # Assuming exam is selected or created first
        
        if not titre or not exam_id:
            messages.error(request, "Veuillez fournir un titre et sélectionner une épreuve.")
            return redirect('compositions:create_composition')

        try:
            exam = Exam.objects.get(id=exam_id)
            # Créez une session de composition ou un enregistrement lié
            # Ici, on suppose qu'il s'agit de créer un nouvel Exam Session (simplifié)
            # Il faudrait une logique plus complexe pour définir les élèves, dates, etc.
            CompositionSession.objects.create(
                exam=exam,
                eleve=request.user, # Placeholder, should be assigned to students
                mode='manuel', # Or similar
                statut=CompositionSession.Statut.NON_COMMENCEE,
                created_by=request.user
            )
            messages.success(request, "Composition créée avec succès.")
            return redirect('compositions:list_compositions')
        except Exam.DoesNotExist:
            messages.error(request, "Épreuve invalide.")
            return redirect('compositions:create_composition')
        except Exception as e:
            messages.error(request, f"Erreur lors de la création: {str(e)}")
            return redirect('compositions:create_composition')
            
    return render(request, 'compositions/create_composition.html')


@login_required
def composition_detail(request, composition_id):
    """Détails d'une composition (pour Prof/Admin)."""
    if request.user.role not in ['professeur', 'admin']:
        return redirect('dashboard')
        
    composition = get_object_or_404(CompositionSession, id=composition_id) # Should probably be Exam object
    
    return render(request, 'compositions/composition_detail.html', {'composition': composition})


@login_required
def submit_paper_view(request, session_id):
    """Soumission de la copie papier pour une session."""
    session = get_object_or_404(CompositionSession, id=session_id, eleve=request.user)
    
    if request.method == 'POST' and request.FILES.getlist('copies'):
        files = request.FILES.getlist('copies')
        
        for i, f in enumerate(files):
            StudentSubmissionFile.objects.create(
                session=session,
                fichier=f,
                page_number=i+1
            )
        
        session.submit()
        
        # Correction IA SYNCHRONE (sans Celery)
        try:
            from .tasks import process_ia_correction_sync
            process_ia_correction_sync(session.id)
        except Exception as e:
            messages.error(request, f"Erreur lors de la correction IA : {str(e)}")
        
        return redirect('compositions:result_detail', session_id=session.id)

    return render(request, 'compositions/submit_paper.html', {'session': session})

@login_required
def result_detail(request, session_id):
    """Affichage du résultat pour l'élève."""
    session = get_object_or_404(CompositionSession, id=session_id, eleve=request.user)
    resultat = getattr(session, 'resultat', None)
    return render(request, 'compositions/result.html', {
        'session': session,
        'resultat': resultat,
    })

@login_required
def ia_corrections_list_view(request):
    """Liste des corrections IA pour les profs/admins."""
    if request.user.role == 'eleve':
        resultats = Resultat.objects.filter(session__eleve=request.user, corrige_par_ia=True)
    elif request.user.role == 'professeur':
        resultats = Resultat.objects.filter(session__exam__createur=request.user, corrige_par_ia=True)
    else: # admin
        resultats = Resultat.objects.filter(corrige_par_ia=True)
        
    return render(request, 'compositions/ia_corrections.html', {'resultats': resultats})
