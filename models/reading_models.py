from pydantic import BaseModel
from typing import List
from uuid import UUID

class ReadingAnswerPayload(BaseModel):
    id: UUID
    answers: List[str]
