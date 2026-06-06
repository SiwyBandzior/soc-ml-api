from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(title="SOC Anomaly Detection API")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, "anomaly_model.pkl")

model = joblib.load(model_path)

class NetworkTraffic(BaseModel):
    packet_size_bytes: float
    session_duration_ms: float


@app.post("/analyze/")
async def analyze_traffic(traffic: NetworkTraffic):
    data_point = np.array([[traffic.packet_size_bytes, traffic.session_duration_ms]])

    prediction = model.predict(data_point)[0]

    score = model.score_samples(data_point)[0]

    is_threat = bool(prediction == -1)

    return {
        "status": "DANGER" if is_threat else "SAFE",
        "thread_detected": is_threat,
        "anomaly_score": round(float(score), 4), 
        "received_data": traffic.dict()
    }