# models/listening_models.py

from pydantic import BaseModel
from typing import List
from uuid import UUID

class ListeningAnswerPayload(BaseModel):
    id: UUID
    answers: List[str]
