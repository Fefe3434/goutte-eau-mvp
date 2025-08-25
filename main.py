from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import date
import os, joblib, numpy as np

MODEL_PATH = os.getenv("MODEL_PATH", "./data/model.joblib")

app = FastAPI(title="Goutte d'eau – MVP", version="0.1.0")

class RiskResponse(BaseModel):
    etat_sol: float
    temps_present: float
    pression_station: float
    temps_passe: float
    nebulosite: float
    pression_mer: float
    humidite: float
    temp_min: float
    prob_rain: float

def load_model():
    return joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

model = load_model()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/risk", response_model=RiskResponse)
def risk(etat_sol: float= Query(...),
        temps_present: float= Query(...),
        pression_station: float= Query(...),
        temps_passe: float= Query(...),
        nebulosite: float= Query(...),
        pression_mer: float= Query(...),
        humidite: float= Query(...),
        temp_min: float= Query(...)):
    X = np.array([[etat_sol, temps_present, pression_station, temps_passe, nebulosite, pression_mer, humidite, temp_min]])

    prob = 0.3
    if model is not None:
        try:
            prob = float(model.predict_proba(X)[0,1])
        except Exception:
            prob = 0.3
    return RiskResponse(etat_sol=etat_sol,
                            temps_present=temps_present,
                            pression_station=pression_station,
                            temps_passe=temps_passe,
                            nebulosite=nebulosite,
                            pression_mer=pression_mer,
                            humidite=humidite,
                            temp_min=temp_min,
                            prob_rain=round(prob, 3))