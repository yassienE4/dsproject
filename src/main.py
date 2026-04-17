from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from feature_extraction import extract_features
from mapping import number_to_type

from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"

model = joblib.load(BASE_DIR / "models" / "best_model.joblib")
scaler = joblib.load(BASE_DIR / "models" / "scaler.joblib")
numerical_cols = joblib.load(BASE_DIR / "models" / "numerical_cols.joblib")

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/predict")
def predict(request: URLRequest):
    features = extract_features(request.url)
    
    df = pd.DataFrame([features])
    df = df[model.feature_names_in_]
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    pred = model.predict(df)[0]
    return {"prediction": number_to_type(pred)}