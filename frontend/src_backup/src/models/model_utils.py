# src/models/model_utils.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def load_dataset(file_path: str):
    """Load CSV dataset safely."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load dataset: {e}")
        return None

def preprocess_features(df: pd.DataFrame, target_col: str):
    """Separate features and target, handle missing values safely."""
    try:
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # --- Separate numeric and categorical ---
        numeric_cols = X.select_dtypes(include=['number']).columns
        categorical_cols = X.select_dtypes(include=['object']).columns

        # Fill numeric missing values with mean
        X[numeric_cols] = X[numeric_cols].fillna(X[numeric_cols].mean())

        # Fill categorical missing values with 'missing' and encode
        for col in categorical_cols:
            X[col] = X[col].fillna('missing')
            X[col] = X[col].astype('category').cat.codes

        return X, y
    except Exception as e:
        print(f"[ERROR] Preprocessing failed: {e}")
        return None, None

def scale_features(X_train, X_test):
    """Scale features and return scaler for production."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

def split_data(X, y, test_size=0.2, random_state=42):
    """Train/test split."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def evaluate_model(y_true, y_pred):
    """Print classification report and confusion matrix."""
    print("[INFO] Classification Report:\n", classification_report(y_true, y_pred))
    print("[INFO] Confusion Matrix:\n", confusion_matrix(y_true, y_pred))