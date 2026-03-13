import pandas as pd
import os

# Input & output paths
RAW_CSV = "data/raw/CICIDS2017.csv"
PROCESSED_CSV = "data/processed/CICIDS2017_processed.csv"

# Columns to drop
columns_to_drop = [
    'flow_id', 'source_ip', 'destination_ip',
    'source_port', 'destination_port',
    'Timestamp', 'Fwd Start Time', 'Bwd Start Time', 'Idle Min'
]

# Make sure processed folder exists
os.makedirs(os.path.dirname(PROCESSED_CSV), exist_ok=True)

# Chunk size to handle large CSV
chunk_size = 500_000
chunks = pd.read_csv(RAW_CSV, chunksize=chunk_size)

processed_chunks = []

print("Starting preprocessing in chunks...")

for i, chunk in enumerate(chunks, start=1):
    # Drop unnecessary columns (only if they exist in this chunk)
    chunk = chunk.drop(columns=[col for col in columns_to_drop if col in chunk.columns])
    
    # Encode attack_label to numeric
    chunk['label_encoded'] = chunk['attack_label'].astype('category').cat.codes
    
    processed_chunks.append(chunk)
    
    print(f"Processed chunk {i} with {len(chunk)} rows")

# Combine all chunks
df_processed = pd.concat(processed_chunks, ignore_index=True)

# Save to processed CSV
df_processed.to_csv(PROCESSED_CSV, index=False)
print(f"✅ Preprocessing complete. Processed CSV saved at: {PROCESSED_CSV}")