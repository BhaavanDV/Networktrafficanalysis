# file: backend/api/live_nids.py
import threading
import asyncio
import time
import joblib
import pandas as pd
import pyshark
from fastapi import FastAPI
from pydantic import BaseModel

# =====================================================
# 1️⃣ FastAPI app
# =====================================================
app = FastAPI(title="Live Network Intrusion Detection API")

# =====================================================
# 2️⃣ Load 3-feature model, scaler, label encoder
# =====================================================
MODEL_PATH = "backend/models/supervised/"

scaler = joblib.load(MODEL_PATH + "scaler_3features.pkl")
model = joblib.load(MODEL_PATH + "rf_model_3features.pkl")
label_encoder = joblib.load(MODEL_PATH + "label_encoder_3features.pkl")

# =====================================================
# 3️⃣ Pydantic model for /predict
# =====================================================
class Packet(BaseModel):
    packet_size: float
    inter_arrival: float
    protocol_encoded: int

# =====================================================
# 4️⃣ /predict endpoint
# =====================================================
@app.post("/predict")
def predict(packet: Packet):
    try:
        # Build dataframe
        live_X = pd.DataFrame([{
            "packet_size": packet.packet_size,
            "inter_arrival": packet.inter_arrival,
            "protocol_encoded": packet.protocol_encoded
        }])
        # Scale
        scaled_X = scaler.transform(live_X)
        # Predict
        pred_class = model.predict(scaled_X)[0]
        # Convert to Python int
        pred_class_py = int(pred_class)
        # Decode label (convert to str)
        pred_label = str(label_encoder.inverse_transform([pred_class])[0])
        # Return safe JSON
        return {"prediction": pred_class_py, "label": pred_label}
    except Exception as e:
        return {"error": str(e)}

# =====================================================
# 5️⃣ Live PyShark capture thread (Windows-safe)
# =====================================================
def capture_live(interface: str = "Ethernet"):
    print(f"[Live Capture] Starting on interface: {interface}")

    # Windows-specific: ensure asyncio loop exists in thread
    asyncio.set_event_loop(asyncio.new_event_loop())

    try:
        cap = pyshark.LiveCapture(interface=interface)
    except Exception as e:
        print("[Error] Failed to start live capture:", e)
        return

    prev_time = None
    for pkt in cap.sniff_continuously():
        try:
            pkt_len = int(pkt.length)
            proto = int(pkt.highest_layer == "TCP") * 6 + int(pkt.highest_layer == "UDP") * 17
            curr_time = float(pkt.sniff_timestamp)
            iat = curr_time - prev_time if prev_time else 0
            prev_time = curr_time

            live_X = pd.DataFrame([{
                "packet_size": pkt_len,
                "inter_arrival": iat,
                "protocol_encoded": proto
            }])
            scaled_X = scaler.transform(live_X)
            pred_class = model.predict(scaled_X)[0]
            pred_label = label_encoder.inverse_transform([pred_class])[0]
            print(f"[Live Prediction] Packet: {pkt_len} bytes, IAT: {iat:.6f}s, Protocol: {proto} -> Prediction: {pred_label}")
        except Exception as e:
            print("[Packet processing error]", e)

# =====================================================
# 6️⃣ Start live capture in background thread on startup
# =====================================================
@app.on_event("startup")
def start_live_capture():
    thread = threading.Thread(target=capture_live, args=("Ethernet",), daemon=True)
    thread.start()
    print("[Startup] Live capture thread started")

# =====================================================
# 7️⃣ Root endpoint
# =====================================================
@app.get("/")
def root():
    return {"message": "Network Intrusion Detection API Running"}