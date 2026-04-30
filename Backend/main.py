from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import PyPDF2
import os
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://resume-ai-analyzer-navy.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "resume_model.pkl")

model_data = joblib.load(MODEL_PATH)

vectorizer = model_data["vectorizer"]
skill_vectors = model_data["skill_vectors"]
df = model_data["df"]


@app.get("/")
def home():
    return {"message": "Resume AI Analyzer backend running with new IT skills model"}


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text.lower()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    resume_text = extract_text_from_pdf(file.file)

    resume_vector = vectorizer.transform([resume_text])

    similarities = cosine_similarity(resume_vector, skill_vectors)[0]

    top_indices = similarities.argsort()[::-1]

    results = []
    seen_jobs = set()

    for index in top_indices:
        score = float(similarities[index])

        if score == 0:
            continue

        row = df.iloc[index]
        job = row["job_role"]

        if job not in seen_jobs:
            seen_jobs.add(job)

            results.append({
                "job": job,
                "score": round(score * 100, 2),
                "matched_skills": row["skills"]
            })

        if len(results) == 5:
            break

    return {
        "top_matches": results
    }