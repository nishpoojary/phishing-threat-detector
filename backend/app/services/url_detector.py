from urllib.parse import urlparse
import re


def analyze_url(url: str):

    indicators = []
    score = 0

    parsed = urlparse(url)

    if not parsed.netloc:
        return {
            "is_suspicious": True,
            "prediction": "SUSPICIOUS",
            "risk_level": "HIGH",
            "risk_score": 100,
            "indicators": ["Invalid URL"],
        }

    # HTTPS
    if parsed.scheme != "https":
        score += 20
        indicators.append("URL does not use HTTPS")

    # IP address
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"

    if re.match(ip_pattern, parsed.hostname or ""):
        score += 30
        indicators.append("IP address used instead of domain")

    # Suspicious words
    suspicious_words = [
        "login",
        "verify",
        "account",
        "secure",
        "password",
        "bank",
        "payment",
        "update",
    ]

    found = [
        word
        for word in suspicious_words
        if word in url.lower()
    ]

    if found:
        score += 25
        indicators.append(
            "Suspicious keywords detected: "
            + ", ".join(found)
        )

    # Long URL
    if len(url) > 100:
        score += 10
        indicators.append("Long URL detected")

    # @ symbol
    if "@" in url:
        score += 20
        indicators.append("@ symbol detected")

    # Risk level
    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MEDIUM"
    elif score >= 20:
        risk_level = "LOW"
    else:
        risk_level = "SAFE"

    if not indicators:
        indicators.append(
            "No suspicious characteristics detected"
        )

    return {
        "is_suspicious": score >= 40,
        "prediction": (
            "SUSPICIOUS"
            if score >= 40
            else "SAFE"
        ),
        "risk_level": risk_level,
        "risk_score": score,
        "indicators": indicators,
    }