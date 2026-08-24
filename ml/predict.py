from pathlib import Path
import joblib


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "phishing_detector.pkl"

print("Loading Model...")

try:
    model = joblib.load(MODEL_PATH)
    print("Model Loaded Successfully!")
except FileNotFoundError:
    print(f"Error: Model file not found at:")
    print(MODEL_PATH)
    exit(1)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)


# --------------------------------------------------
# Email prediction
# --------------------------------------------------

while True:

    print("\n" + "=" * 60)

    email_text = input(
        "\nEnter Email Content (or type 'exit' to quit):\n\n"
    ).strip()

    if email_text.lower() == "exit":
        print("\nGoodbye!")
        break

    if not email_text:
        print("\nPlease enter some email content.")
        continue

    try:
        # Make prediction
        prediction = model.predict([email_text])[0]

        # Get probabilities
        probability = model.predict_proba([email_text])[0]

        # Probability mapping
        safe_score = round(probability[0] * 100, 2)
        phishing_score = round(probability[1] * 100, 2)

        # Display result
        print("\n" + "-" * 60)
        print("RESULT")
        print("-" * 60)

        if prediction == 1:
            print("⚠️  PHISHING EMAIL DETECTED")
        else:
            print("✅  SAFE EMAIL")

        print(f"\nPhishing Probability : {phishing_score}%")
        print(f"Safe Probability     : {safe_score}%")

        print("-" * 60)

    except Exception as e:
        print(f"\nPrediction Error: {e}")