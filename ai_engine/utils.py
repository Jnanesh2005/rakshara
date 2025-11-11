import joblib
import numpy as np
import os
from django.conf import settings

# Paths to model files
MODEL_PATH = os.path.join(settings.BASE_DIR, 'ai_engine', 'model', 'model.joblib')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'ai_engine', 'model', 'scaler.joblib')

# Load model and scaler once at startup
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ AI model and scaler loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading AI model: {e}")
    model, scaler = None, None


def predict_health(hr, spo2, br, temp, weight, height):
    """
    Predict health status using Isolation Forest.
    Returns: (score, label)
    """
    if model is None or scaler is None:
        return 0.0, "Model Not Loaded"

    # Calculate BMI safely
    try:
        height_m = float(height) / 100
        bmi = float(weight) / (height_m ** 2)
    except Exception:
        bmi = 18.5

    # Dummy attendance %
    attendance_percentage = 95.0

    # Convert input to match model format
    features = np.array([[temp * 9/5 + 32,  # °C → °F
                          float(spo2),
                          float(hr),
                          float(bmi),
                          attendance_percentage]])

    # Scale
    scaled_features = scaler.transform(features)

    # Predict with IsolationForest
    prediction = model.predict(scaled_features)[0]  # -1 = anomaly, 1 = normal
    score = model.decision_function(scaled_features)[0]

    # Label conversion
    if prediction == 1:
        label = "Healthy"
    elif score > -0.1:
        label = "Mild"
    else:
        label = "Critical"

    norm_score = round((1 - abs(score)) * 100, 2)
    return norm_score, label
