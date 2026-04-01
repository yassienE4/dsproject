from fastapi import FastAPI
from feature_extraction import extract_features
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("best_model.joblib")

@app.post("/predict")
def predict(url: str):

    features = extract_features(url)
    
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    
    return {"prediction": int(pred)}