import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.utils import resample
import logging
import os

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# -------------------------
# Paths
# -------------------------
RAW_CSV = "data/processed/CICIDS2017_final.csv"
OUTPUT_DIR = "data/processed/ML_ready"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Load dataset
# -------------------------
logger.info(f"Loading dataset from {RAW_CSV} ...")
df = pd.read_csv(RAW_CSV)
logger.info(f"Dataset shape: {df.shape}")
logger.info(f"Label distribution:\n{df['label_encoded'].value_counts()}")

# -------------------------
# Separate features and target
# -------------------------
X = df.drop(columns=['attack_label', 'label_encoded', 'protocol'])
y = df['label_encoded']

# -------------------------
# Train-test split
# -------------------------
logger.info("Splitting data into train/test sets ...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
logger.info(f"Train shape: {X_train.shape}, Test shape: {X_test.shape}")

# -------------------------
# Feature scaling
# -------------------------
logger.info("Applying StandardScaler ...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
logger.info("Feature scaling complete.")

# -------------------------
# Downsample majority class
# -------------------------
logger.info("Downsampling majority class for faster SMOTE ...")
majority_class = 0  # assuming '0' is majority
majority_mask = y_train == majority_class
minority_mask = ~majority_mask

X_majority = X_train_scaled[majority_mask]
X_minority = X_train_scaled[minority_mask]
y_majority = y_train[majority_mask]
y_minority = y_train[minority_mask]

# Downsample majority to 500k samples
X_majority_down = resample(
    X_majority,
    replace=False,
    n_samples=500_000,
    random_state=42
)
y_majority_down = np.zeros(500_000, dtype=y_train.dtype)

# Combine downsampled majority with all minority
X_train_small = np.vstack([X_majority_down, X_minority])
y_train_small = np.hstack([y_majority_down, y_minority])

logger.info(f"New training shape before SMOTE: {X_train_small.shape}")

# -------------------------
# Apply SMOTE on minority classes only
# -------------------------
logger.info("Applying SMOTE to balance minority classes ...")
os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # limit cores if needed
smote = SMOTE(random_state=42, sampling_strategy='minority', k_neighbors=3)
X_train_res, y_train_res = smote.fit_resample(X_train_small, y_train_small)
logger.info(f"Training shape after SMOTE: {X_train_res.shape}")

# -------------------------
# Save datasets
# -------------------------
logger.info(f"Saving .npy datasets to {OUTPUT_DIR} ...")
np.save(os.path.join(OUTPUT_DIR, "X_train.npy"), X_train_res)
np.save(os.path.join(OUTPUT_DIR, "y_train.npy"), y_train_res)
np.save(os.path.join(OUTPUT_DIR, "X_test.npy"), X_test_scaled)
np.save(os.path.join(OUTPUT_DIR, "y_test.npy"), y_test.to_numpy())
logger.info("All datasets saved successfully ✅")