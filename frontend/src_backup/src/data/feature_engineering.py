# src/data/feature_engineering.py
import pandas as pd

# List of features your model was trained on
MODEL_FEATURES = [
    "ACK Flag Count",
    "Active Mean",
    "Average Packet Size",
    "Avg Bwd Segment Size",
    "Avg Fwd Segment Size",
    "Flow Duration",
    "Fwd Packet Length Mean",
    "Bwd Packet Length Mean",
    # ... include all features from your training set
]

def transform(raw_packet: dict) -> pd.DataFrame:
    """
    Converts raw packet dictionary into a DataFrame
    with the same features used during model training.
    """
    # Example computations (replace with your real logic)
    features = {
        "ACK Flag Count": raw_packet.get("ack_flags", 0),
        "Active Mean": raw_packet.get("active_mean", 0),
        "Average Packet Size": raw_packet.get("packet_size", 0),
        "Avg Bwd Segment Size": raw_packet.get("bwd_segment_size", 0),
        "Avg Fwd Segment Size": raw_packet.get("fwd_segment_size", 0),
        "Flow Duration": raw_packet.get("flow_duration", 0),
        "Fwd Packet Length Mean": raw_packet.get("fwd_packet_len_mean", 0),
        "Bwd Packet Length Mean": raw_packet.get("bwd_packet_len_mean", 0),
        # ... fill all other features
    }

    # Make a single-row DataFrame
    df = pd.DataFrame([features])

    # Ensure columns are in the same order as during training
    return df[MODEL_FEATURES]