from pydantic import BaseModel
from typing import List

class ReadingAnswerPayload(BaseModel):
    id: str
    answers: List[str]  # e.g., ["A", "C", "D", "B", "C"]
