from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from frontend

# Use eventlet for async socket handling
socketio = SocketIO(app, cors_allowed_origins="*")

# Simple HTTP route to test
@app.route("/")
def index():
    return "Backend is running!"

# SocketIO event
@socketio.on("connect")
def handle_connect():
    print(f"🟢 Client connected: {request.sid}")
    emit("message", {"data": f"Connected with socket id {request.sid}"})

@socketio.on("disconnect")
def handle_disconnect():
    print(f"🔴 Client disconnected: {request.sid}")

@socketio.on("ping_from_client")
def handle_ping(data):
    print(f"Ping received from client: {data}")
    emit("pong_from_server", {"data": "Pong!"})

import random
import time

def generate_traffic():
    while True:
        data = {
            "timestamp": time.strftime("%H:%M:%S"),
            "src_ip": f"192.168.1.{random.randint(1,255)}",
            "dst_ip": f"10.0.0.{random.randint(1,255)}",
            "protocol": random.choice(["TCP","UDP","ICMP"]),
            "packet_size": random.randint(64,1500),
            "prediction": random.choice([0,1])
        }

        socketio.emit("traffic_update", data)

        socketio.sleep(2)

socketio.start_background_task(generate_traffic)

if __name__ == "__main__":
    # Run on port 5000 (make sure it's free)
    socketio.run(app, host="0.0.0.0", port=5000)