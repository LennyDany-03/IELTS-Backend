from fastapi import APIRouter, HTTPException
from services.listening_service import get_random_listening_set, evaluate_listening_answers
from models.listening_models import ListeningAnswerPayload
import traceback  # 👈 Add this for detailed error output

router = APIRouter(prefix="/api/listening", tags=["Listening"])

@router.get("/practice")
def get_random_listening():
    """
    🎧 Get a random listening practice set:
    - audio_url
    - questions (array of MCQs)
    """
    try:
        return get_random_listening_set()
    except Exception as e:
        traceback.print_exc()  # 🔍 Logs full stack trace to console
        raise HTTPException(status_code=500, detail=f"Failed to fetch practice set: {str(e)}")


@router.post("/submit")
def submit_listening(payload: ListeningAnswerPayload):
    """
    ✅ Submit user's answers for evaluation.
    - Returns score and feedback.
    """
    try:
        return evaluate_listening_answers(payload)
    except Exception as e:
        traceback.print_exc()  # 🔍 Logs full stack trace to console
        raise HTTPException(status_code=400, detail=f"Evaluation failed: {str(e)}")
