import pandas as pd
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "it_jobs_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "resume_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

df.columns = df.columns.str.strip()

df = df.dropna(subset=["job_role", "skills"])

df["job_role"] = df["job_role"].astype(str)
df["skills"] = df["skills"].astype(str).str.lower()

vectorizer = TfidfVectorizer()
skill_vectors = vectorizer.fit_transform(df["skills"])

model_data = {
    "vectorizer": vectorizer,
    "skill_vectors": skill_vectors,
    "df": df
}

joblib.dump(model_data, MODEL_PATH)

print("Model trained successfully!")
print("Saved at:", MODEL_PATH)
print("Total rows:", len(df))
print("Total job roles:", df["job_role"].nunique())