import pandas as pd

chunk_size = 500_000
chunks = pd.read_csv("data/raw/CICIDS2017.csv", chunksize=chunk_size)

# Collect label counts
label_counts = {}

for chunk in chunks:
    counts = chunk['attack_label'].value_counts()
    for label, count in counts.items():
        label_counts[label] = label_counts.get(label, 0) + count

print(label_counts)