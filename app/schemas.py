from pydantic import BaseModel
from typing import Dict, List


class TrainRequest(BaseModel):
    project_id: int
    intents: Dict[str, List[str]]

class PredictRequest(BaseModel):
    project_id: int
    text: str

class PredictResponse(BaseModel):
    intent: str | None
    confidence: float
    alternatives: list
    entities: Dict[str, List[str]]
