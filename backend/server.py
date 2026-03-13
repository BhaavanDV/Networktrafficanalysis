from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
import random
import time

app = Flask(__name__)
CORS(app)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# ------------------ Data Storage ------------------ #
traffic_data = []

# ------------------ Socket.IO Events ------------------ #

@socketio.on("connect")
def handle_connect():
    print(f"Client connected: {request.sid}")

    # Send last 50 packets to new client
    for pkt in traffic_data[-50:]:
        socketio.emit("traffic_update", pkt, to=request.sid)


@socketio.on("disconnect")
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")


# ------------------ API Endpoints ------------------ #

@app.route("/")
def index():
    return jsonify({
        "message": "Network Traffic Analysis Backend Running"
    })


@app.route("/traffic")
def get_traffic():
    return jsonify(traffic_data[-50:])


@app.route("/predict_attack", methods=["POST"])
def predict_attack():

    data = request.json

    src_ip = data.get("src_ip", "Unknown")
    dst_ip = data.get("dst_ip", "Unknown")

    attack_type = random.choice([
        "Normal",
        "DDoS",
        "Port Scan",
        "Brute Force",
        "SQL Injection"
    ])

    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

        "source_ip": src_ip,
        "destination_ip": dst_ip,

        "attack_name": attack_type,

        "attack_category": "Known"
        if attack_type in ["DDoS", "Port Scan", "Brute Force"]
        else "Unknown",

        "prediction": 1 if attack_type != "Normal" else 0,

        "confidence": round(random.uniform(0.80, 0.99), 2),

        "model": random.choice([
            "RandomForest",
            "SVM",
            "NeuralNet",
            "XGBoost"
        ]),

        "accuracy": round(random.uniform(0.90, 0.98), 2)
    }

    return jsonify(result)


# ------------------ Traffic Generator ------------------ #

def generate_traffic():

    while True:

        src_ip = f"192.168.1.{random.randint(1,254)}"
        dst_ip = f"10.0.0.{random.randint(1,254)}"

        attack_type = random.choice([
            "Normal",
            "DDoS",
            "Port Scan",
            "Brute Force",
            "SQL Injection"
        ])

        pkt = {

            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),

            "source_ip": src_ip,
            "destination_ip": dst_ip,

            "attack_name": attack_type,

            "attack_category": "Known"
            if attack_type in ["DDoS", "Port Scan", "Brute Force"]
            else "Unknown",

            "prediction": 1 if attack_type != "Normal" else 0,

            "confidence": round(random.uniform(0.80, 0.99), 2),

            "model": random.choice([
                "RandomForest",
                "SVM",
                "NeuralNet",
                "XGBoost"
            ]),

            "accuracy": round(random.uniform(0.90, 0.98), 2)
        }

        traffic_data.append(pkt)

        # Send to frontend
        socketio.emit("traffic_update", pkt)

        time.sleep(1)


# ------------------ Start Server ------------------ #

if __name__ == "__main__":

    print("Starting Network Traffic Backend...")

    # Start traffic generator thread
    threading.Thread(
        target=generate_traffic,
        daemon=True
    ).start()

    # Run Socket.IO server
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000
    )