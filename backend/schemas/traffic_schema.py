from pydantic import BaseModel
from typing import Dict

class TrafficInput(BaseModel):

    features: Dict[str, float]

    model_type: str = "rf"


class PredictionResponse(BaseModel):

    attack_type: str
    confidence: float
    category: str
    model_type: str