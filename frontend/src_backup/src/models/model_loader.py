# src/models/model_loader.py
import os
import joblib

# Paths to saved model, scaler, and features
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
MODEL_FILE = os.path.join(MODEL_DIR, "network_model.pkl")
SCALER_FILE = os.path.join(MODEL_DIR, "scaler.pkl")
FEATURES_FILE = os.path.join(MODEL_DIR, "features.pkl")

def load_model():
    """Load model, scaler, and features."""
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(f"Model file not found at {MODEL_FILE}")
    if not os.path.exists(SCALER_FILE):
        raise FileNotFoundError(f"Scaler file not found at {SCALER_FILE}")
    if not os.path.exists(FEATURES_FILE):
        raise FileNotFoundError(f"Features file not found at {FEATURES_FILE}")

    model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    features = joblib.load(FEATURES_FILE)
    return model, scaler, features