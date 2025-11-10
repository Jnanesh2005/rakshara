# WARNING: This is a simple heuristic model for demonstration.
# Not medical advice. Use proper clinical models for production.

def predict_health(heart_rate, spo2, breathing_rate, temperature_c, weight_kg=None, height_cm=None):
    """
    Returns (score, label)
    score: 0-100 where higher means more concerning (risk)
    label: 'Normal', 'Watch', 'High Risk'
    Simple rules:
    - spo2: <92 increases risk heavily
    - temp > 38 increases risk
    - heart rate > 110 or < 50 increases risk
    - breathing_rate > 22 increases risk
    - BMI outliers increase slightly
    """
    score = 0.0

    # SpO2
    if spo2 is None:
        score += 5
    elif spo2 < 85:
        score += 50
    elif spo2 < 92:
        score += 30
    elif spo2 < 95:
        score += 10

    # Temperature
    if temperature_c is None:
        score += 2
    elif temperature_c >= 40:
        score += 40
    elif temperature_c >= 38:
        score += 20
    elif temperature_c >= 37.5:
        score += 8

    # Heart rate
    if heart_rate is None:
        score += 2
    else:
        if heart_rate < 50:
            score += 20
        elif heart_rate <= 100:
            score += 0
        elif heart_rate <= 120:
            score += 15
        else:
            score += 30

    # Breathing rate
    if breathing_rate is None:
        score += 2
    elif breathing_rate > 30:
        score += 30
    elif breathing_rate > 22:
        score += 15

    # BMI effect (optional)
    if weight_kg and height_cm:
        try:
            h_m = height_cm / 100.0
            bmi = weight_kg / (h_m * h_m)
            if bmi < 16 or bmi > 35:
                score += 10
            elif bmi < 18.5 or bmi > 30:
                score += 5
        except Exception:
            pass

    # clamp and build label
    if score < 10:
        label = "Normal"
    elif score < 30:
        label = "Watch"
    else:
        label = "High Risk"

    if score > 100: score = 100.0
    return round(score, 1), label
