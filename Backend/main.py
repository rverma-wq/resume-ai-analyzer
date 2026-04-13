from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import joblib
import PyPDF2

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML model
model = joblib.load("model/resume_model.pkl")


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    return text


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    pdf_text = extract_text_from_pdf(file.file)

    prediction = model.predict([pdf_text])[0]

    return {"prediction": prediction}