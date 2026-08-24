import pandas as pd

print("Script Started")

df = pd.read_csv("dataset/phishing_email.csv")

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())

print("\nLabel Distribution:")
print(df["label"].value_counts())
