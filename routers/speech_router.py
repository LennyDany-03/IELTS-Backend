from fastapi import APIRouter
from pydantic import BaseModel
from services.openai_client import evaluate_speaking_transcript

speech_router = APIRouter()


class TranscriptRequest(BaseModel):
    transcript: str


@speech_router.post("/evaluate-transcript")
async def evaluate_transcript(data: TranscriptRequest):
    """
    Accepts a spoken transcript as text and returns structured IELTS feedback.
    """
    try:
        feedback = evaluate_speaking_transcript(data.transcript)
        return {
            "transcript": data.transcript,
            "feedback": feedback
        }
    except Exception as e:
        print(f"[❌ Transcript Evaluation Error]: {e}")
        return {"error": f"Speech evaluation failed: {str(e)}"}


@speech_router.get("/evaluate-transcript")
async def check_speech_api():
    """
    Health check for frontend to verify backend is reachable.
    """
    return {"message": "Speech API is reachable"}
