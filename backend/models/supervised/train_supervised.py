import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Load your training dataset
df = pd.read_csv("../../dataset/your_supervised_data.csv")  # adjust path
X_train = df.drop(columns=["attack_label"])
y_train = df["attack_label"]

# Train model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Save model
os.makedirs("backend/models/supervised", exist_ok=True)
joblib.dump(rf, "backend/models/supervised/rf_model.pkl")

# Save feature columns for later use in HybridDetector
features_columns = X_train.columns.tolist()
joblib.dump(features_columns, "backend/models/supervised/supervised_features_columns.pkl")

print("Supervised model and features saved successfully!")