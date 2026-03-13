import pandas as pd

def extract_features(df_packets: pd.DataFrame, features: list) -> pd.DataFrame:
    """
    Converts raw packet DataFrame into model-ready features.
    - df_packets: DataFrame with raw packet info
    - features: list of features expected by the model
    """
    df = pd.DataFrame()

    # Example numeric mapping
    df["Flow Duration"] = 0  # placeholder
    df["Total Fwd Packets"] = df_packets["bytes_sent"]
    df["Total Backward Packets"] = df_packets["bytes_received"]
    df["Total Length of Fwd Packets"] = df_packets["packet_size"]
    df["Inter Arrival"] = df_packets["inter_arrival"]

    # ---------------------------
    # Handle categorical features
    # ---------------------------
    # Protocol: map to integers
    protocol_map = {"TCP": 1, "UDP": 2, "ICMP": 3}
    if "protocol" in features:
        df["protocol"] = df_packets["protocol"].map(protocol_map).fillna(0)

    # ---------------------------
    # Fill missing features with 0
    # ---------------------------
    for f in features:
        if f not in df.columns:
            df[f] = 0

    # Ensure column order matches model
    return df[features]