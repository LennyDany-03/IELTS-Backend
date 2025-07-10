from fastapi import APIRouter, HTTPException
from services.reading_service import get_random_reading_set, evaluate_reading_answers
from models.reading_models import ReadingAnswerPayload

router = APIRouter(prefix="/api/reading", tags=["Reading"])

@router.get("/practice")
def get_reading_quiz():
    try:
        return get_random_reading_set()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit")
def submit_reading_quiz(payload: ReadingAnswerPayload):
    try:
        return evaluate_reading_answers(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
