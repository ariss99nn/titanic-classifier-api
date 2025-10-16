import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Cargar el modelo
MODEL_PATH = "model.joblib"
model = joblib.load(MODEL_PATH)

app = FastAPI()

class Passenger(BaseModel):
    pclass: int
    sex: str
    age: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(passenger: Passenger):
    data = [[passenger.pclass, passenger.sex, passenger.age]]
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # 👈 Railway le pasa este valor
    uvicorn.run(app, host="0.0.0.0", port=port)
