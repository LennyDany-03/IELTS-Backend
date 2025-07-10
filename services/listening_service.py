from services.supabase_client import supabase
import random

def get_random_listening_set():
    data = supabase.table("listening_sets").select("*").execute()
    items = data.data
    if not items:
        return {"error": "No listening sets available"}
    return random.choice(items)

def evaluate_listening_answers(payload):
    # Fetch correct answers from Supabase
    data = supabase.table("listening_sets").select("correct").eq("id", str(payload.id)).single().execute()
    correct = data.data["correct"]
    user = payload.answers

    # Calculate score
    score = sum([1 for u, c in zip(user, correct) if u == c])
    
    # Create feedback array: "✅" if correct, "❌" otherwise
    feedback = ["✅" if u == c else "❌" for u, c in zip(user, correct)]

    return {
        "score": score,
        "total": len(correct),
        "feedback": feedback,  # ✅ Frontend expects this
        "band_estimate": convert_score_to_band(score, len(correct))
    }

def convert_score_to_band(score, total):
    percent = score / total
    if percent >= 0.9: return 9
    elif percent >= 0.8: return 8
    elif percent >= 0.7: return 7
    elif percent >= 0.6: return 6
    return 5
