# src/live_capture.py
import pyshark
import pandas as pd
from ml_service import preprocess_features, predict_attack  # your existing model functions

def capture_live(interface="Wi-Fi", packet_count=50):
    capture = pyshark.LiveCapture(interface=interface)
    packets_data = []

    print(f"Capturing {packet_count} packets from {interface}...")
    for i, pkt in enumerate(capture.sniff_continuously(packet_count=packet_count)):
        pkt_dict = {
            "f0": len(pkt),  # simple example: packet length
            "f1": int(pkt.highest_layer == "TCP"),
            "f2": int(pkt.highest_layer == "UDP"),
            # add more feature extraction logic matching your model
        }
        packets_data.append(pkt_dict)

    df_live = pd.DataFrame(packets_data)
    df_features = preprocess_features(df_live)
    predictions = predict_attack(df_features)
    print(predictions)

if __name__ == "__main__":
    capture_live()