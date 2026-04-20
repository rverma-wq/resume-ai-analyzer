from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import PyPDF2
import os

app = FastAPI()

# CORS (temporary open)
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

# Safe model loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model", "resume_model.pkl")

model = joblib.load(model_path)


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text


@app.get("/")
def home():
    return {"message": "Resume AI Analyzer backend running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    pdf_text = extract_text_from_pdf(file.file)
    prediction = model.predict([pdf_text])[0]
    return {"prediction": prediction}