import pandas as pd
import random
import datetime
import os

# Absolute path to data/processed folder
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
output_dir = os.path.join(project_root, "data", "processed")
os.makedirs(output_dir, exist_ok=True)

# Generate simulated network traffic data
data = []
now = datetime.datetime.now()
for i in range(1000):
    data.append({
        "timestamp": now + datetime.timedelta(seconds=i),
        "packet_size": random.randint(40, 1500),
        "protocol": random.choice([1, 6, 17]),  # ICMP, TCP, UDP
        "inter_arrival": round(random.random(), 3),
        "anomaly": random.choice([0, 1])
    })

df = pd.DataFrame(data)
output_file = os.path.join(output_dir, "network_data.csv")
df.to_csv(output_file, index=False)

print(f"✅ network_data.csv created at {output_file}")