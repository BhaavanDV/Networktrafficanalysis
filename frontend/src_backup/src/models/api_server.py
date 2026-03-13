from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from src.models.model_loader import load_model
from src.utils.feature_extractor import extract_features
from scapy.all import sniff
import pandas as pd
import asyncio

app = FastAPI(title="Network Traffic Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Load ML model, scaler, features once
model, scaler, features = load_model()
print("[INFO] Model, scaler, and features loaded successfully!")

# Keep WebSocket clients
clients = set()

# ----------------------------
# WebSocket endpoint for live alerts
# ----------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print(f"[INFO] Client connected: {websocket.client}")
    try:
        while True:
            await asyncio.sleep(1)  # keep connection alive
    except Exception as e:
        print(f"[ERROR] WebSocket: {e}")
    finally:
        clients.remove(websocket)
        await websocket.close()
        print(f"[INFO] Client disconnected: {websocket.client}")

# ----------------------------
# Function to send predictions to all connected clients
# ----------------------------
async def send_to_clients(prediction):
    for ws in clients.copy():  # use copy to avoid modification during iteration
        try:
            await ws.send_json(prediction)
        except:
            pass  # skip disconnected clients

# ----------------------------
# Scapy live packet capture
# ----------------------------
def process_packet(packet):
    df_packet = pd.DataFrame([{
        "timestamp": str(packet.time),
        "src_ip": getattr(packet[0][1], "src", "0.0.0.0"),
        "dst_ip": getattr(packet[0][1], "dst", "0.0.0.0"),
        "bytes_sent": len(packet),
        "packet_size": len(packet),
        "protocol": getattr(packet, "proto", "TCP"),
    }])

    # Extract features
    X = extract_features(df_packet, features)
    X_scaled = scaler.transform(X)
    pred = model.predict(X_scaled)[0]

    prediction = {
        "timestamp": str(packet.time),
        "src_ip": df_packet["src_ip"][0],
        "dst_ip": df_packet["dst_ip"][0],
        "packet_size": df_packet["packet_size"][0],
        "protocol": df_packet["protocol"][0],
        "prediction": int(pred)
    }

    # Schedule sending to WebSocket clients
    for ws in clients.copy():
        asyncio.create_task(send_to_clients(prediction))

# ----------------------------
# Background task to run Scapy sniffing
# ----------------------------
def start_sniffing():
    print("[INFO] Starting live packet capture...")
    sniff(prn=process_packet, store=False)

# ----------------------------
# Startup event to run live sniffing in background
# ----------------------------
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, start_sniffing)
    print("[INFO] Background packet sniffing started")