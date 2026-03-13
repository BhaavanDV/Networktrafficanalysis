from backend.detection.supervised_detector import SupervisedDetector

# Load model ONCE (very important for performance)
detector = SupervisedDetector(model_type="rf")

def predict_traffic(features):
    prediction = detector.predict(features)
    proba = detector.predict_proba(features)

    confidence = float(proba.max())

    return {
        "attack_type": prediction[0],
        "confidence": round(confidence, 3),
        "category": "known"
    }