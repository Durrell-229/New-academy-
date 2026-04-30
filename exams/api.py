from ninja import Router
from .models import Exam
from typing import List
from ninja import Schema
import uuid

router = Router()

class ExamSchema(Schema):
    id: uuid.UUID
    titre: str
    type_exam: str
    duree_minutes: int

@router.get("/", response=List[ExamSchema])
def list_exams(request):
    return Exam.objects.all()
