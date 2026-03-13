# src/train/train_rf.py

import os
import numpy as np
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import resample
import joblib

# -------------------------
# ✅ Logging setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# -------------------------
# 1️⃣ Paths and model directory
# -------------------------
DATA_DIR = "data/processed/ML_ready"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "random_forest_fast.pkl")

# -------------------------
# 2️⃣ Load datasets
# -------------------------
logger.info("Loading ML-ready datasets...")
X_train = np.load(os.path.join(DATA_DIR, "X_train.npy"))
y_train = np.load(os.path.join(DATA_DIR, "y_train.npy"))
X_test = np.load(os.path.join(DATA_DIR, "X_test.npy"))
y_test = np.load(os.path.join(DATA_DIR, "y_test.npy"))

logger.info(f"X_train: {X_train.shape} y_train: {y_train.shape}")
logger.info(f"X_test: {X_test.shape} y_test: {y_test.shape}")

# -------------------------
# 3️⃣ Downsample majority class for fast training
# -------------------------
logger.info("Downsampling training data to 500000 rows for fast training...")
majority_mask = y_train == 0
minority_mask = y_train != 0

X_majority = X_train[majority_mask]
y_majority = y_train[majority_mask]
X_minority = X_train[minority_mask]
y_minority = y_train[minority_mask]

X_majority_down = resample(
    X_majority,
    n_samples=500_000,
    random_state=42
)
y_majority_down = np.zeros(500_000, dtype=y_train.dtype)

X_train_small = np.vstack([X_majority_down, X_minority])
y_train_small = np.hstack([y_majority_down, y_minority])

logger.info(f"Training shape after downsampling: {X_train_small.shape}")

# -------------------------
# 4️⃣ Train RandomForest
# -------------------------
logger.info("Training RandomForest on subset...")
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)
rf.fit(X_train_small, y_train_small)
logger.info("RandomForest training complete ✅")

# -------------------------
# 5️⃣ Evaluate model
# -------------------------
logger.info("Evaluating model on test set...")
y_pred = rf.predict(X_test)
logger.info("\nClassification Report:\n" + classification_report(y_test, y_pred))
logger.info(f"Confusion Matrix shape: {confusion_matrix(y_test, y_pred).shape}")

# -------------------------
# 6️⃣ Save trained model
# -------------------------
logger.info(f"Saving trained model to {MODEL_PATH} ...")
joblib.dump(rf, MODEL_PATH)
logger.info("Model saved successfully ✅")