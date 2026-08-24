import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


DATASET_PATH = "dataset/phishing_email.csv"
MODEL_PATH = "ml/phishing_detector.pkl"


print("Loading Dataset...")

df = pd.read_csv(DATASET_PATH)

df["text_combined"] = df["text_combined"].fillna("")

X = df["text_combined"]
y = df["label"]


print("Splitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("Building Model...")

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=100000,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            random_state=42
        )
    )
])


print("Training Started...")

model.fit(X_train, y_train)

print("Training Completed!")


predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:")
print(f"{accuracy * 100:.2f} %")


print("\nClassification Report:")
print(classification_report(y_test, predictions))


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))


joblib.dump(model, MODEL_PATH)

print(f"\nModel saved as {MODEL_PATH}")