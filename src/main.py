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

@app.post("/predict")
def predict(request: URLRequest):
    features = extract_features(request.url)
    
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    print(extract_features("https://google.com"))
    print(extract_features("https://facebook.com"))
    print(extract_features("http://very-bad-phishing-site123.biz/login"))
    return {"prediction": number_to_type(pred)}