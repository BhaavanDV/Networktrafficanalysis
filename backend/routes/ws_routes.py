# backend/routes/ws_routes.py
from fastapi import APIRouter, WebSocket
from backend.detection.hybrid_detector import HybridDetector
import pandas as pd
import json

router = APIRouter()
hd = HybridDetector()

@router.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            features = json.loads(data)
            pred = hd.predict(pd.DataFrame([features]))[0]
            await websocket.send_json(pred)
    except:
        await websocket.close()