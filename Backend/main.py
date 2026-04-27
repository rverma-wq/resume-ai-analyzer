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
        "https://resume-ai-analyzer-navy.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

vectorizer = joblib.load(os.path.join(BASE_DIR, "model", "vectorizer.pkl"))
job_vectors = joblib.load(os.path.join(BASE_DIR, "model", "job_vectors.pkl"))
job_data = joblib.load(os.path.join(BASE_DIR, "model", "job_data.pkl"))


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text


@app.get("/")
def home():
    return {"message": "Resume AI Analyzer backend running with new model"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file.file)

    resume_vector = vectorizer.transform([pdf_text])
    similarities = cosine_similarity(resume_vector, job_vectors)[0]

    top_indices = similarities.argsort()[-5:][::-1]

    results = []
    print(job_data.columns)
    for i in top_indices:
        row = job_data.iloc[i]

        results.append({
            "job": row.iloc[0],
            "score": round(float(similarities[i]) * 100, 2)
        })

    return {"results": results}