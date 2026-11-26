from pathlib import Path
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="API de Predicción de Precios de Viviendas")


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "linear_model.joblib"


try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = None



class ViviendaInput(BaseModel):
    m2: float = Field(..., gt=0, description="Superficie de la vivienda en m2")



@app.get("/")
def health_check():
    return {
        "status": "OK",
        "message": "API de Predicción de Precios de Viviendas está en funcionamiento.",
        "model_loaded": model is not None,
    }



@app.get("/predict")
def predict_get(m2: float = Query(..., gt=0, description="Superficie en m2")):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    prediccion = float(model.predict(np.array([[m2]]))[0])
    return {
        "m2": m2,
        "precio_estimado": round(prediccion, 2),
        "moneda": "COP",
    }


@app.post("/predict")
def predict_post(datos: ViviendaInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo no cargado")

    prediccion = float(model.predict(np.array([[datos.m2]]))[0])
    return {
        "m2": datos.m2,
        "precio_estimado": round(prediccion, 2),
        "moneda": "COP",
    }