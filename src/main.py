from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import joblib
import numpy as np
import os
import csv
from datetime import datetime
from sklearn.ensemble import IsolationForest

app = FastAPI(title="SOC Anomaly Detection API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "anomaly_model.pkl")
LOG_FILE_PATH = os.path.join(BASE_DIR, "traffic_logs.csv")

model = joblib.load(MODEL_PATH)

class NetworkTraffic(BaseModel):
    packet_size_bytes: float
    session_duration_ms: float

def save_log_to_csv(traffic_data: dict, is_threat: bool, score: float):
    file_exists = os.path.isfile(LOG_FILE_PATH)
    
    with open(LOG_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "packet_size_bytes", "session_duration_ms", "is_threat", "anomaly_score"])
        
        writer.writerow([
            datetime.utcnow().isoformat(),
            traffic_data["packet_size_bytes"],
            traffic_data["session_duration_ms"],
            is_threat,
            score
        ])

@app.post("/analyze/")
async def analyze_traffic(traffic: NetworkTraffic, background_tasks: BackgroundTasks):
    data_point = np.array([[traffic.packet_size_bytes, traffic.session_duration_ms]])
    
    prediction = model.predict(data_point)[0]
    score = model.score_samples(data_point)[0]
    is_threat = bool(prediction == -1)
    
    background_tasks.add_task(save_log_to_csv, traffic.dict(), is_threat, round(float(score), 4))
    
    return {
        "status": "DANGER" if is_threat else "SAFE",
        "threat_detected": is_threat,
        "anomaly_score": round(float(score), 4),
        "received_data": traffic.dict()
    }

@app.post("/retrain/")
async def retrain_model():
    if not os.path.isfile(LOG_FILE_PATH):
        return {"status": "error", "message": "No network logs found for retraining."}
    
    training_data = []
    with open(LOG_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            training_data.append([
                float(row["packet_size_bytes"]), 
                float(row["session_duration_ms"])
            ])
            
    if len(training_data) < 10:
        return {"status": "warning", "message": f"Not enough data. Have {len(training_data)}/10 required logs."}
        
    X_train = np.array(training_data)
    new_model = IsolationForest(contamination=0.05, random_state=42)
    new_model.fit(X_train)
    
    joblib.dump(new_model, MODEL_PATH)
    
    global model
    model = new_model
    
    return {
        "status": "success", 
        "message": f"AI successfully retrained on {len(training_data)} real network logs!"
    }