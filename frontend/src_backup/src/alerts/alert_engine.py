def generate_alert(prediction, src_ip):
    if prediction == 1:
        return {
            "alert": True,
            "type": "DDoS / Anomaly",
            "impact": f"User {src_ip} causing abnormal traffic",
            "severity": "HIGH"
        }
    return {"alert": False}