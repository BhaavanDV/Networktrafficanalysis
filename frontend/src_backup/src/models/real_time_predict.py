# src/models/real_time_predict.py
import os
import pandas as pd
import numpy as np
from model_loader import load_model

# --- CONFIG ---
DATA_PATH = "src/datasets/network_data.csv"  # Live/raw network data
MODEL, SCALER = load_model()                 # Load saved model & scaler

def preprocess_live_data(df: pd.DataFrame):
    """
    Preprocess incoming live network data.
    For now, extract numeric features similar to training.
    """
    try:
        # Drop timestamp & IPs (model trained on numeric features)
        df_processed = df.drop(columns=['timestamp', 'src_ip', 'dst_ip'], errors='ignore')

        # Fill missing numeric values
        df_processed = df_processed.fillna(df_processed.mean())

        # Encode categorical columns if any (like protocol)
        for col in df_processed.select_dtypes(include=['object']).columns:
            df_processed[col] = df_processed[col].astype('category').cat.codes

        return df_processed
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")
        return None

def predict_live(df: pd.DataFrame):
    """Predict attacks for live network data."""
    X_processed = preprocess_live_data(df)
    if X_processed is None:
        return None

    try:
        X_scaled = SCALER.transform(X_processed)
        predictions = MODEL.predict(X_scaled)
        df['predicted_label'] = predictions
        return df
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return None

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Live data file not found: {DATA_PATH}")
        exit(1)

    # Load live network data
    live_df = pd.read_csv(DATA_PATH)

    # Predict attacks
    result_df = predict_live(live_df)
    if result_df is not None:
        print("[INFO] Predictions added to dataframe:")
        print(result_df.head())

        # Optionally, save predictions
        result_df.to_csv("src/datasets/network_data_predicted.csv", index=False)
        print("[SUCCESS] Predictions saved to network_data_predicted.csv")