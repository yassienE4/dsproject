from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("model/random_forest_model.pkl")

@app.post("/predict")
def predict(url: str):
    # simple placeholder (use your real feature extraction)
    features = {
        "url_length": len(url)
    }
    
    df = pd.DataFrame([features])
    pred = model.predict(df)[0]
    
    return {"prediction": int(pred)}