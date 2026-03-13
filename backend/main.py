# ==========================
# main.py
# ==========================
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import socketio
import asyncio
import traceback
import sys
import os
from typing import Dict, Any, List, Optional

# Add backend/src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "services"))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "detection"))

from services.feature_pipeline import build_features
from detection.supervised_detector import SupervisedDetector
from services.live_capture_service import start_capture_thread

# ==========================
# FastAPI + Socket.IO
# ==========================
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app = FastAPI(title="Network IDS API (Batch + Top-N)", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
asgi_app = socketio.ASGIApp(sio, app)

# ==========================
# Attack mapping
# ==========================
ATTACK_MAPPING = {
    0: "Normal",
    1: "DoS",
    2: "Probe",
    3: "R2L",
    4: "U2R"
}

# ==========================
# Dynamic prediction function
# ==========================
def dynamic_prediction(input_json: Dict[str, Any], model_type: str = "rf", top_n: int = 1) -> Dict[str, Any]:
    """
    Predict attack for any JSON input.
    top_n: return top N predictions
    """
    try:
        features = input_json.get("features", input_json)
        detector = SupervisedDetector(model_type=model_type)
        # Fill missing features with 0
        full_features = {f: float(features.get(f, 0.0)) for f in detector.feature_names}
        df_features = pd.DataFrame([full_features])

        # Predict
        prediction = detector.predict(df_features)
        pred_proba = detector.predict_proba(df_features)

        # Top-N predictions
        if pred_proba is not None:
            probs = pred_proba[0]  # single row
            top_indices = probs.argsort()[::-1][:top_n]
            top_predictions = []
            for idx in top_indices:
                top_predictions.append({
                    "attack_type": str(idx),
                    "attack_name": ATTACK_MAPPING.get(idx, "Unknown"),
                    "confidence": float(probs[idx])
                })
        else:
            top_predictions = [{
                "attack_type": str(prediction[0]),
                "attack_name": ATTACK_MAPPING.get(int(prediction[0]), "Unknown"),
                "confidence": 1.0
            }]

        category = "known" if int(prediction[0]) in ATTACK_MAPPING else "unknown"

        return {
            "input": input_json,
            "top_predictions": top_predictions,
            "model_type": model_type,
            "category": category
        }

    except Exception as e:
        return {"error": str(e), "input": input_json}

# ==========================
# Single dynamic prediction
# ==========================
@app.post("/predict")
def predict_endpoint(
    data: Dict[str, Any],
    top_n: int = Query(1, description="Return top N predictions per input")
):
    model_type = data.get("model_type", "rf")
    return dynamic_prediction(data, model_type=model_type, top_n=top_n)

# ==========================
# Batch dynamic prediction
# ==========================
@app.post("/predict_batch")
def predict_batch_endpoint(
    data_list: List[Dict[str, Any]],
    top_n: int = Query(1, description="Return top N predictions per input")
):
    results = []
    for data in data_list:
        model_type = data.get("model_type", "rf")
        results.append(dynamic_prediction(data, model_type=model_type, top_n=top_n))
    return {"predictions": results}

# ==========================
# Health check
# ==========================
@app.get("/")
def home():
    return {"message": "Network IDS API Running"}