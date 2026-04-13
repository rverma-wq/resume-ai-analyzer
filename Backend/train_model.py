import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Clean text function
def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\W", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

df = pd.read_csv("data/resume_data.csv", encoding="utf-8-sig")

# Clean column names
df.columns = df.columns.str.strip()

print("Columns:", df.columns)

# Find the correct job column automatically
target_col = [c for c in df.columns if "job_position" in c][0]
print("Target column detected:", target_col)

df = df.dropna(subset=[target_col])

# Remove rows with empty skills
df = df.dropna(subset=["skills"])

# Combine useful text fields
df["combined_text"] = (
    df["skills"].fillna("") + " " +
    df["career_objective"].fillna("") + " " +
    df["major_field_of_studies"].fillna("")
)

df["cleaned_resume"] = df["combined_text"].apply(clean_text)

# Features and labels
X = df["cleaned_resume"]
# Find the correct label column automatically
target_col = [c for c in df.columns if "job_position_name" in c][0]
print("Using target column:", target_col)

y = df[target_col]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ML pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=5000)),
    ("model", LogisticRegression(max_iter=1000))
])

# Train
pipeline.fit(X_train, y_train)

# Evaluate
predictions = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# Save model
joblib.dump(pipeline, "model/resume_model.pkl")

print("Model saved successfully!")