# Frontend

This folder contains the single-page dashboard served by FastAPI.

## What it shows

- A URL input form that calls `POST /predict`
- Prediction result styling for the four classes: benign, defacement, malware, phishing
- Notebook-backed evaluation visuals, including the tuned model confusion matrix
- Model summary cards based on the evaluation notebook
- A feature-signal tag panel that mirrors the backend feature extractor

## Files

- `index.html`: page structure
- `styles.css`: visual design and layout
- `app.js`: prediction logic and chart rendering

## Run

Start the API from `src` and open the root page in the browser. The frontend is served from the same FastAPI app, so the UI and `/predict` endpoint share one origin.