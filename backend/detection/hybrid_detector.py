import os
import joblib
import numpy as np
import pandas as pd


class HybridDetector:
    def __init__(self):

        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models"))

        # Load supervised model
        self.rf_model = joblib.load(os.path.join(base_dir, "rf_model.pkl"))

        # Load label encoder
        self.label_encoder = joblib.load(os.path.join(base_dir, "label_encoder.pkl"))

        # Load feature columns
        self.supervised_features = joblib.load(
            os.path.join(base_dir, "supervised_features_columns.pkl")
        )

        # Load unsupervised model
        self.iso_model = joblib.load(os.path.join(base_dir, "iso_model.pkl"))

    def predict(self, packet_features: pd.DataFrame):

        results = []

        df = packet_features.copy()

        # Ensure required columns exist
        for col in self.supervised_features:
            if col not in df.columns:
                df[col] = 0

        # Reorder columns
        df = df[self.supervised_features]

        # Supervised prediction
        rf_preds = self.rf_model.predict(df)
        rf_probs = self.rf_model.predict_proba(df)

        # Unsupervised prediction
        iso_preds = self.iso_model.predict(df)

        for i in range(len(df)):

            rf_label = rf_preds[i]
            rf_confidence = max(rf_probs[i])

            attack_name = self.label_encoder.inverse_transform([rf_label])[0]

            # High confidence supervised result
            if rf_confidence >= 0.85:

                results.append({
                    "attack_type": attack_name,
                    "confidence": round(float(rf_confidence), 2),
                    "category": "known"
                })

            else:
                # Use Isolation Forest
                if iso_preds[i] == -1:

                    results.append({
                        "attack_type": "Unknown Attack",
                        "confidence": round(float(1 - rf_confidence), 2),
                        "category": "unknown"
                    })

                else:

                    results.append({
                        "attack_type": "Normal",
                        "confidence": 0.99,
                        "category": "normal"
                    })

        return results