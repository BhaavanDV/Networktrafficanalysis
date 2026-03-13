# backend/models/unsupervised/train_isolation_forest.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

# Load dataset
data = pd.read_csv(r"C:\Users\bhaav\Downloads\Networktrafficanalysis\src\datasets\CICIDS2017_final.csv")

# Drop non-numeric / irrelevant columns
drop_cols = ["label", "attack_type", "Src IP", "Dst IP", "Flow ID"]  # adjust if needed
data = data.drop(columns=[col for col in drop_cols if col in data.columns])

# Convert Protocol to numeric
if 'Protocol' in data.columns:
    data['Protocol'] = data['Protocol'].map({'TCP': 0, 'UDP': 1, 'ICMP': 2}).fillna(0)

# Convert other categorical columns to dummy variables
data = pd.get_dummies(data)

# Train Isolation Forest
iso = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
iso.fit(data)

# Save model
os.makedirs("backend/models/unsupervised", exist_ok=True)
joblib.dump(iso, "backend/models/unsupervised/isolation_forest.pkl")

# ✅ Save feature columns for later use
features_columns = data.columns.tolist()
joblib.dump(features_columns, "backend/models/unsupervised/iso_features_columns.pkl")

print("Isolation Forest trained and saved successfully!")