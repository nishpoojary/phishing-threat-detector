from pathlib import Path
import joblib
import re

# --------------------------------------------------
# Load trained model
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "ml" / "phishing_detector.pkl"

try:
    model = joblib.load(MODEL_PATH)
    print("Phishing detection model loaded successfully!")
except Exception as e:
    model = None
    print(f"Failed to load phishing detection model: {e}")


# --------------------------------------------------
# Detection indicators
# --------------------------------------------------

def analyze_indicators(subject: str, body: str) -> list[str]:

    text = f"{subject} {body}".lower()

    indicators = []

    urgent_words = [
        "urgent",
        "immediately",
        "action required",
        "act now",
        "within 24 hours",
        "expires",
        "final warning",
    ]

    reward_words = [
        "won",
        "winner",
        "prize",
        "gift card",
        "reward",
        "lottery",
        "free money",
    ]

    credential_words = [
        "password",
        "verify your account",
        "login",
        "sign in",
        "credentials",
        "confirm your identity",
    ]

    financial_words = [
        "bank",
        "credit card",
        "payment",
        "account number",
        "transaction",
        "refund",
    ]

    link_words = [
        "click here",
        "click the link",
        "open the link",
        "verify now",
    ]

    if any(word in text for word in urgent_words):
        indicators.append("Urgent or threatening language detected")

    if any(word in text for word in reward_words):
        indicators.append("Prize or reward-related language detected")

    if any(word in text for word in credential_words):
        indicators.append("Account or credential request detected")

    if any(word in text for word in financial_words):
        indicators.append("Financial information-related language detected")

    if any(word in text for word in link_words):
        indicators.append("Suspicious call-to-action detected")

    urls = re.findall(r"https?://[^\s]+", text)

    if urls:
        indicators.append("External URL detected")

    if not indicators:
        indicators.append("No obvious suspicious indicators detected")

    return indicators


# --------------------------------------------------
# Main detection function
# --------------------------------------------------

def detect_phishing(subject: str, body: str) -> dict:

    if model is None:
        raise RuntimeError("Phishing detection model is not available.")

    email_text = f"{subject}\n{body}"

    prediction = model.predict([email_text])[0]

    probabilities = model.predict_proba([email_text])[0]

    safe_probability = round(float(probabilities[0]) * 100, 2)
    phishing_probability = round(float(probabilities[1]) * 100, 2)

    is_phishing = bool(prediction == 1)

    if phishing_probability >= 90:
        risk_level = "CRITICAL"
    elif phishing_probability >= 70:
        risk_level = "HIGH"
    elif phishing_probability >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    indicators = analyze_indicators(subject, body)

    return {
        "is_phishing": is_phishing,
        "prediction": "PHISHING" if is_phishing else "SAFE",
        "phishing_probability": phishing_probability,
        "safe_probability": safe_probability,
        "risk_level": risk_level,
        "indicators": indicators,
    }