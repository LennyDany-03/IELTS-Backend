from fastapi import APIRouter
from models.essay import Essay
from services.openai_client import get_essay_feedback

essay_router = APIRouter()

@essay_router.post("/evaluate-essay")
async def evaluate_essay(data: Essay):
    try:
        feedback = get_essay_feedback(data.text)  # ✅ no await here
        return {"feedback": feedback}
    except Exception as e:
        print(f"[Essay Feedback Error]: {e}")
        return {"error": "Failed to evaluate essay."}

