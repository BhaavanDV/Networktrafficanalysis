import joblib
import pandas as pd
from pathlib import Path
from config.features import FEATURE_NAMES
print(len(FEATURE_NAMES))  # Must be 71
print(FEATURE_NAMES)       # Should match training order exactly

class SupervisedDetector:
    def __init__(self, model_type="rf"):
        """
        Load model, scaler, and label encoder.
        model_type: str, one of the trained models ('rf', 'xgb', 'lr', etc.)
        """
        BASE_DIR = Path(__file__).resolve().parents[1]
        MODEL_DIR = BASE_DIR / "models"

        # Load model
        model_path = MODEL_DIR / f"{model_type}_model.pkl"
        print("Loading model:", model_path)
        self.model = joblib.load(model_path)

        # Load scaler if exists
        scaler_path = MODEL_DIR / "scaler.pkl"
        self.scaler = joblib.load(scaler_path) if scaler_path.exists() else None

        # Load label encoder if exists
        le_path = MODEL_DIR / "label_encoder.pkl"
        self.label_encoder = joblib.load(le_path) if le_path.exists() else None

        # All features used by the model
        self.feature_names = FEATURE_NAMES

    def _prepare_input(self, X):
        """
        Convert input to DataFrame with all features in correct order.
        Missing features filled with 0. Columns reindexed for model.
        """
        if isinstance(X, dict):
            X = pd.DataFrame([X])

        # Convert all to numeric
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        # Reindex columns to match training feature order, fill missing with 0
        X = X.reindex(columns=self.feature_names, fill_value=0)

        # Apply scaler if available
        if self.scaler:
            X = self.scaler.transform(X)

        return X

    def predict(self, X):
        """
        Return predicted label(s) as string(s)
        """
        X_prepared = self._prepare_input(X)
        pred = self.model.predict(X_prepared)

        if self.label_encoder:
            pred = self.label_encoder.inverse_transform(pred)

        return pred

    def predict_proba(self, X):
        """
        Return predicted probabilities for each class
        """
        X_prepared = self._prepare_input(X)
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X_prepared)
        return None