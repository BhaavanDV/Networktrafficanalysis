import os
import pandas as pd
from nids_datasets import Dataset, DatasetInfo

# Create raw directory
os.makedirs("data/raw", exist_ok=True)

info = DatasetInfo(dataset="CIC-IDS2017")
print(info)

dataset = Dataset(
    dataset="CIC-IDS2017",
    subset=["Network-Flows"],
    files=["all"]
)

dataset.download()

parquet_dir = os.path.join("CIC-IDS2017", "Network-Flows")

parquet_files = [
    os.path.join(parquet_dir, f)
    for f in os.listdir(parquet_dir)
    if f.endswith(".parquet")
]

df_list = []
for p in parquet_files:
    print("Loading:", p)
    df_list.append(pd.read_parquet(p))

df = pd.concat(df_list, ignore_index=True)

save_path = os.path.join("data", "raw", "CICIDS2017.csv")
df.to_csv(save_path, index=False)

print("Saved CICIDS2017 CSV at:", save_path)