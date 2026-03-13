import numpy as np

# Load ML-ready datasets
X_train = np.load("data/processed/ML_ready/X_train.npy")
y_train = np.load("data/processed/ML_ready/y_train.npy")
X_test = np.load("data/processed/ML_ready/X_test.npy")
y_test = np.load("data/processed/ML_ready/y_test.npy")

# Print shapes to confirm
print("X_train:", X_train.shape, "y_train:", y_train.shape)
print("X_test:", X_test.shape, "y_test:", y_test.shape)