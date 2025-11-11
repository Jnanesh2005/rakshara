# ai_engine/translate.py

# --- MULTILINGUAL TRANSLATIONS ---

translations = {
    "en": {
        "FEVER_DETECTED": "Fever Detected",
        "LOW_OXYGEN": "Low Oxygen Saturation",
        "HIGH_PULSE": "High Pulse Rate (Tachycardia)",
        "LOW_PULSE": "Low Pulse Rate (Bradycardia)",
        "AI_ANOMALY": "AI anomaly detected",
        "REC_FEVER": "Student should visit the school nurse for follow-up.",
        "REC_LOW_OXYGEN": "URGENT: Student requires immediate medical check by a professional.",
        "REC_HIGH_PULSE": "Check if student was running. If at rest, monitor closely and inform nurse.",
        "REC_LOW_PULSE": "Student should be seen by the school nurse for monitoring.",
        "REC_AI_ANOMALY": "Subtle anomaly detected. Recommend teacher or counselor to check well-being.",
        "REC_NORMAL": "All vitals appear normal."
    },
    "kn": {
        "FEVER_DETECTED": "ಜ್ವರ ಪತ್ತೆಯಾಗಿದೆ",
        "LOW_OXYGEN": "ಕಡಿಮೆ ಆಮ್ಲಜನಕದ ಶುದ್ಧತ್ವ",
        "HIGH_PULSE": "ಅಧಿಕ ನಾಡಿ ಬಡಿತ (ಟಾಕಿಕಾರ್ಡಿಯಾ)",
        "LOW_PULSE": "ಕಡಿಮೆ ನಾಡಿ ಬಡಿತ (ಬ್ರಾಡಿಕಾರ್ಡಿಯಾ)",
        "AI_ANOMALY": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆಯಿಂದ ಅಸಂಗತತೆ ಪತ್ತೆಯಾಗಿದೆ",
        "REC_FEVER": "ವಿದ್ಯಾರ್ಥಿಯು ಶಾಲೆಯ ನರ್ಸ್ ಅನ್ನು ಭೇಟಿ ಮಾಡಬೇಕು.",
        "REC_LOW_OXYGEN": "ತುರ್ತು: ವಿದ್ಯಾರ್ಥಿಗೆ ತಕ್ಷಣದ ವೈದ್ಯಕೀಯ ತಪಾಸಣೆ ಅಗತ್ಯವಿದೆ.",
        "REC_HIGH_PULSE": "ವಿದ್ಯಾರ್ಥಿ ಓಡುತ್ತಿದ್ದಾನೆಯೆ ಎಂದು ಪರಿಶೀಲಿಸಿ. ವಿಶ್ರಾಂತಿಯಲ್ಲಿದ್ದರೆ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ.",
        "REC_LOW_PULSE": "ವಿದ್ಯಾರ್ಥಿಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆಗಾಗಿ ನರ್ಸ್ ನೋಡಬೇಕು.",
        "REC_AI_ANOMALY": "ಆರೋಗ್ಯ ಅಸಂಗತತೆ ಪತ್ತೆಯಾಗಿದೆ. ಪೋಷಕರಿಗೆ ತಿಳಿಸಿ ಮತ್ತು ವಿದ್ಯಾರ್ಥಿಯನ್ನು ಗಮನಿಸಿ.",
        "REC_NORMAL": "ಎಲ್ಲಾ ಪ್ರಮುಖ ಚಿಹ್ನೆಗಳು ಸಾಮಾನ್ಯವಾಗಿವೆ."
    },
    "hi": {
        "FEVER_DETECTED": "बुखार का पता चला",
        "LOW_OXYGEN": "कम ऑक्सीजन स्तर",
        "HIGH_PULSE": "उच्च नाड़ी दर (टैकीकार्डिया)",
        "LOW_PULSE": "कम नाड़ी दर (ब्रैडीकार्डिया)",
        "AI_ANOMALY": "AI द्वारा असामान्यता का पता चला",
        "REC_FEVER": "छात्र को स्कूल नर्स से मिलना चाहिए।",
        "REC_LOW_OXYGEN": "अत्यावश्यक: छात्र को तुरंत चिकित्सा जांच की आवश्यकता है।",
        "REC_HIGH_PULSE": "जांचें कि क्या छात्र दौड़ रहा था। यदि नहीं, तो निगरानी करें।",
        "REC_LOW_PULSE": "छात्र को निगरानी के लिए नर्स से मिलना चाहिए।",
        "REC_AI_ANOMALY": "स्वास्थ्य पैटर्न असामान्यता पाई गई। माता-पिता को सूचित करें।",
        "REC_NORMAL": "सभी संकेत सामान्य हैं।"
    }
}


def get_translated_text(key, lang='en'):
    """Get a translated message or fallback to English."""
    return translations.get(lang, translations['en']).get(key, key)
