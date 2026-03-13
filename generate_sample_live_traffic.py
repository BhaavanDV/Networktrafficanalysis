import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)
N = 5  # number of rows

# Random "Normal" traffic
normal_data = np.random.rand(N, 70) * 0.5

# Random "Attack" traffic
attack_data = np.random.rand(N, 70) * 2 + 1  # larger values simulate abnormal patterns

# Combine and create labels for reference (won't be used by ml_service)
features = np.vstack([normal_data, attack_data])
df = pd.DataFrame(features, columns=[f"f{i}" for i in range(70)])
df["label"] = ["Normal"]*N + ["Attack"]*N

# Save CSV
sample_csv = "data/sample_live_traffic.csv"
df.to_csv(sample_csv, index=False)
print(f"Sample traffic CSV saved to {sample_csv}")