# backend/detection/unsupervised_detector.py
import joblib
import pandas as pd
import numpy as np
import os

import os
import joblib

class UnsupervisedDetector:
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/unsupervised"))
        self.model = joblib.load(os.path.join(base_dir, "isolation_forest.pkl"))
        self.features_columns = joblib.load(os.path.join(base_dir, "iso_features_columns.pkl"))

    def isolation_forest_predict(self, df: pd.DataFrame):
        # Add missing columns with 0
        for col in self.features_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training
        df = df[self.features_columns]
        
        preds = self.model.predict(df)
        return ["anomaly" if p == -1 else "normal" for p in preds]
def isolation_forest_predict(self, df: pd.DataFrame):
    # Convert Protocol to numeric if exists
    if "Protocol" in df.columns:
        df["Protocol"] = df["Protocol"].map({"TCP": 0, "UDP": 1, "ICMP": 2}).fillna(0)
    
    # Drop non-numeric columns
    df = df.select_dtypes(include=[np.number])

    # Add missing columns with 0
    for col in self.features_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder columns to match training
    df = df[self.features_columns]

    # Predict
    preds = self.model.predict(df)
    scores = self.model.decision_function(df)
    max_score, min_score = np.max(scores), np.min(scores)
    confidences = [(s - min_score)/(max_score - min_score + 1e-8) for s in scores]

    result = []
    for p, conf in zip(preds, confidences):
        result.append({
            "prediction": "anomaly" if p == -1 else "normal",
            "confidence": round(conf, 2)
        })
    return result