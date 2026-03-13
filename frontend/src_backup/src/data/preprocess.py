import pandas as pd

# File paths
input_csv = "data/processed/CICIDS2017_processed.csv"
output_csv = "data/processed/CICIDS2017_final.csv"

# Columns to drop
drop_cols = [
    "flow_id", "source_ip", "destination_ip", "source_port", "destination_port",
    "Timestamp", "Idle Min", "Idle Max", "Idle Std", "Active Min", "Active Max", "Active Std"
]

# Load CSV in chunks to handle large file
chunk_size = 500_000
chunks = pd.read_csv(input_csv, chunksize=chunk_size)

processed_chunks = []

print("Starting final preprocessing in chunks...")

for i, chunk in enumerate(chunks, 1):
    # Drop unnecessary columns (if they exist)
    cols_to_drop = [c for c in drop_cols if c in chunk.columns]
    chunk = chunk.drop(columns=cols_to_drop)

    # Encode attack labels to numeric (0 = BENIGN, 1+ = attack types)
    if "label_encoded" not in chunk.columns:
        chunk["label_encoded"] = chunk["attack_label"].astype('category').cat.codes

    processed_chunks.append(chunk)
    print(f"Processed chunk {i} with {len(chunk)} rows")

# Combine all chunks
final_df = pd.concat(processed_chunks, ignore_index=True)

# Save final cleaned CSV
final_df.to_csv(output_csv, index=False)
print(f"✅ Final preprocessing complete. Saved cleaned CSV at: {output_csv}")

# Quick sanity check
print("\nColumn names:", final_df.columns.tolist())
print("Label distribution:\n", final_df['label_encoded'].value_counts())