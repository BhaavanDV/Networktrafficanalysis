import joblib
import pandas as pd
import os

# Path to your CSV dataset
data_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../src/datasets/CICIDS2017_final.csv")
)

# Load the dataset
df = pd.read_csv(data_path)

# Extract feature columns (exclude the target column if present)
if "Label" in df.columns:
    features_columns = [col for col in df.columns if col != "Label"]
else:
    features_columns = df.columns.tolist()

# Save path
save_path = os.path.join(os.path.dirname(__file__), "supervised_features_columns.pkl")

# Save features columns
joblib.dump(features_columns, save_path)
print(f"supervised_features_columns.pkl saved successfully at {save_path}!")