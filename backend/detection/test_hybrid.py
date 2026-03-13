import pandas as pd
from .hybrid_detector import HybridDetector
from backend.detection.hybrid_detector import HybridDetector

hd = HybridDetector()

# Example packet
packet = pd.DataFrame([
    {"Src IP": "192.168.1.2", "Dst IP": "8.8.8.8", "Protocol": "TCP", "Packet Size": 500}
])

results = hd.predict(packet)
print(results)