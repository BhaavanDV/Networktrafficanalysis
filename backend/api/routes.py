# backend/api/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from services.feature_pipeline import build_features
from detection.hybrid_detector import HybridDetector

router = APIRouter()
detector = HybridDetector()

class Packet(BaseModel):
    packet_size: float
    inter_arrival: float
    protocol_encoded: int

@router.post("/predict")
def predict(packet: Packet):
    features = build_features(packet.packet_size, packet.inter_arrival, packet.protocol_encoded)
    pred_class = detector.predict(features)[0]
    return {"prediction": pred_class}