# app.py
import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

import pandas as pd

app = FastAPI(title="Titanic Classifier")

# Cargar modelo (pipeline)
MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
model = joblib.load(MODEL_PATH)

# Definir el schema de entrada (ejemplo)
class PredictRequest(BaseModel):
    pclass: int
    sex: str
    age: Optional[float] = None
    sibsp: Optional[int] = 0
    parch: Optional[int] = 0
    fare: Optional[float] = None
    embarked: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: PredictRequest):
    data = pd.DataFrame([payload.dict()])
    probs = model.predict_proba(data)[0]
    pred = int(model.predict(data)[0])
    return {
        "prediction": pred,
        "probability": float(probs[pred]),
        "probabilities": {"0": float(probs[0]), "1": float(probs[1])}
    }