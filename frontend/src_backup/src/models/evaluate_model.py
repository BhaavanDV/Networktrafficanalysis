# src/models/evaluate_model.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

MODEL_FILE = "src/models/saved_models/network_model.pkl"
SCALER_FILE = "src/models/saved_models/scaler.pkl"

def load_model_and_scaler(model_path=MODEL_FILE, scaler_path=SCALER_FILE):
    """Load saved model and scaler."""
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError("[ERROR] Model or scaler not found. Train first!")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def load_dataset(file_path: str, target_col: str):
    """Load CSV dataset safely and split features/target."""
    try:
        df = pd.read_csv(file_path)
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # Fill missing numeric values
        X = X.fillna(X.mean())

        # Encode categorical features if any
        for col in X.select_dtypes(include=['object']).columns:
            X[col] = X[col].astype('category').cat.codes

        return X, y
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        return None, None

def evaluate(model, scaler, X, y):
    """Scale features, predict, and print evaluation metrics."""
    try:
        X_scaled = scaler.transform(X)
        y_pred = model.predict(X_scaled)
        print("[INFO] Classification Report:\n", classification_report(y, y_pred))
        print("[INFO] Confusion Matrix:\n", confusion_matrix(y, y_pred))
    except Exception as e:
        print(f"[ERROR] Evaluation failed: {e}")

if __name__ == "__main__":
    DATA_PATH = "src/datasets/CICIDS2017_final.csv"
    TARGET_COL = "label_encoded"

    # --- Load model & scaler ---
    model, scaler = load_model_and_scaler()

    # --- Load evaluation dataset ---
    X, y = load_dataset(DATA_PATH, TARGET_COL)
    if X is None or y is None:
        exit(1)

    # --- Evaluate ---
    evaluate(model, scaler, X, y)