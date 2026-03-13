# backend/services/feature_pipeline.py
import pandas as pd

def build_features(packet_size, inter_arrival, protocol_encoded):
    return pd.DataFrame([{
        "packet_size": packet_size,
        "inter_arrival": inter_arrival,
        "protocol_encoded": protocol_encoded
    }])