import os
import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# =====================================================
# 1️⃣ Get Project Root Path
# =====================================================
BASE_DIR = Path(__file__).resolve().parents[2]

data_path = BASE_DIR / "src" / "datasets" / "CICIDS2017_final.csv"
model_path = BASE_DIR / "backend" / "models" / "supervised"

os.makedirs(model_path, exist_ok=True)
print("Dataset path:", data_path)

# =====================================================
# 2️⃣ Load Dataset
# =====================================================
df = pd.read_csv(data_path)

# =====================================================
# 3️⃣ Clean Dataset
# =====================================================
df.replace([float("inf"), float("-inf")], pd.NA, inplace=True)
df.dropna(inplace=True)

# =====================================================
# 4️⃣ Select 3 Live-Capturable Features
# =====================================================
selected_features = ["packet_size", "inter_arrival", "protocol_encoded"]
X = df[selected_features]
print("Using selected features:", X.shape)

# =====================================================
# 5️⃣ Encode Labels
# =====================================================
y = df.iloc[:, -1]  # last column assumed label
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# =====================================================
# 6️⃣ Scale Features
# =====================================================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =====================================================
# 7️⃣ Train-Test Split
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# =====================================================
# 8️⃣ Train Random Forest
# =====================================================
rf_model = RandomForestClassifier(
    n_estimators=50,
    max_depth=20,
    n_jobs=-1,
    random_state=42
)
rf_model.fit(X_train, y_train)

# =====================================================
# 9️⃣ Train XGBoost
# =====================================================
xgb_model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    eval_metric="mlogloss",
    tree_method="hist",
    n_jobs=-1
)
xgb_model.fit(X_train, y_train)

# =====================================================
# 🔟 Evaluation
# =====================================================
print("\nRandom Forest Report:")
print(classification_report(y_test, rf_model.predict(X_test)))

print("\nXGBoost Report:")
print(classification_report(y_test, xgb_model.predict(X_test)))

# =====================================================
# 1️⃣1️⃣ Save Models & Scaler
# =====================================================
joblib.dump(rf_model, model_path / "rf_model.pkl")
joblib.dump(xgb_model, model_path / "xgb_model.pkl")
joblib.dump(label_encoder, model_path / "label_encoder.pkl")
joblib.dump(scaler, model_path / "scaler.pkl")

print("\n✅ All models saved successfully!")