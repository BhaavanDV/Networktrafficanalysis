from sklearn.ensemble import IsolationForest
import numpy as np

model = IsolationForest(contamination=0.05, random_state=42)

# train dummy baseline model
X = np.random.rand(1000,3)
model.fit(X)

def predict(packet_size, protocol_id, port):

    data = [[packet_size, protocol_id, port]]

    result = model.predict(data)

    # sklearn returns
    # 1 = normal
    # -1 = anomaly

    if result[0] == -1:
        return 1   # attack
    else:
        return 0   # normal