from fastapi import FastAPI
from feature_extraction import extract_features
import joblib
import pandas as pd
from mapping import number_to_type, type_to_number

from pydantic import BaseModel

class URLRequest(BaseModel):
    url: str

app = FastAPI()

model = joblib.load("../models/best_model.joblib")
scaler = joblib.load("../models/scaler.joblib")
numerical_cols = joblib.load("../models/numerical_cols.joblib")

@app.post("/predict")
def predict(request: URLRequest):
    features = extract_features(request.url)
    
    df = pd.DataFrame([features])
    df = df[model.feature_names_in_]
    df[numerical_cols] = scaler.transform(df[numerical_cols])
    pred = model.predict(df)[0]
    return {"prediction": number_to_type(pred)}