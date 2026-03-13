import pandas as pd
from unsupervised_detector import UnsupervisedDetector

# Example test packet
test_packet = pd.DataFrame([{
    "Flow Duration": 100,
    "Fwd Packet Count": 5,
    "Bwd Packet Count": 2,
    "Average Packet Size": 200,
    "Protocol": "TCP"
}])

# Initialize detector
ud = UnsupervisedDetector()

# Predict
result = ud.isolation_forest_predict(test_packet)
print(result)