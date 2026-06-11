```python
readme_content = """# 🛡️ Enterprise SOC Anomaly Detection System

An end-to-end MLOps solution for real-time network traffic anomaly detection. This system utilizes an **Isolation Forest** machine learning model to analyze network packet attributes, flags potential threats (e.g., DDoS, data exfiltration), logs live traffic in the background, and supports **hot-swappable continuous retraining** without server downtime.

Developed as a production-ready portfolio project demonstrating full-stack AI/ML integration, containerization, and security operation center (SOC) automation.

---

## 🏗️ Architecture & System Workflow

1. **Frontend Dashboard (Streamlit):** An intuitive user interface for network analysts to input packet size and session duration, inspect live AI confidence scores, and trigger administrative retraining.
2. **Backend API (FastAPI & Docker):** A high-performance, asynchronous REST API containerized with Docker. It serves predictions and executes non-blocking background logging tasks.
3. **Continuous Training (MLOps Pipeline):** Incoming requests are logged dynamically to a CSV data store inside the container. When the administrator triggers a retrain, the model re-learns from history and updates server memory instantly with zero downtime.

---

## 🚀 Key Features

- **Real-Time Threat Intelligence:** Instantly classifies network traffic into `SAFE` or `DANGER` (Anomaly).
- **Asynchronous Background Logging:** Leverages FastAPI `BackgroundTasks` to log incoming telemetry data seamlessly without increasing request latency.
- **Hot-Swappable Retraining Pipeline:** Trains a new `IsolationForest` model on collected production logs and swaps the active model in memory on-the-fly.
- **Production Containerization:** Fully containerized architecture using Docker, ensuring consistency across development and production environments.
- **Professional Security Theme:** Sleek dark-mode compatible Streamlit interface optimized for SOC operations.

---

## 🛠️ Tech Stack

- **Core Language:** Python 3.11
- **Machine Learning:** Scikit-Learn, NumPy, Joblib
- **Backend Framework:** FastAPI, Uvicorn, Pydantic
- **Frontend Dashboard:** Streamlit, Requests
- **DevOps & Infrastructure:** Docker

---

## 📁 Project Structure


```

```text
File generated successfully as README.md

```text
soc-ml-api/
├── src/
│   └── main.py             # FastAPI Application (API endpoints, logging & hot-swap retraining)
├── train_model.py          # Initial cold-start synthetic model training script
├── dashboard.py            # Streamlit user interface & administrative control panel
├── Dockerfile              # Docker recipe for the backend API & ML model environment
├── .dockerignore           # Excludes environments and temporary caches from Docker build
├── .gitignore              # Protects repository from heavy files (*.pkl) and virtual environments
├── requirements.txt        # Production dependencies python manifest
└── README.md               # System documentation (This file)

```

---

## 🔧 Installation & Setup

### Prerequisites

* Python 3.11+
* Docker Desktop installed and running

### 1. Environment Setup (Local Testing)

Clone the repository and set up a virtual environment:

```bash
git clone [https://github.com/your-username/soc-ml-api.git](https://github.com/your-username/soc-ml-api.git)
cd soc-ml-api
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt

```

### 2. Cold-Start Model Training

Generate the initial synthetic baseline model:

```bash
python3 train_model.py

```

### 3. Containerize & Run the Backend API

Build the production Docker image and spin up the container:

```bash
# Remove any conflicting containers
docker rm -f soc-ai-server

# Build the image skipping cache to ensure fresh deployment
docker build --no-cache -t soc-ml-api-container .

# Run the container mapping port 8000
docker run -d -p 8000:8000 --name soc-ai-server soc-ml-api-container

```

Verify the API is live by navigating to the interactive Swagger docs: `http://127.0.0.1:8000/docs`

### 4. Launch the SOC Dashboard

With the Docker container active in the background, run the Streamlit frontend:

```bash
streamlit run dashboard.py

```

Open your browser at `http://localhost:8501` to access the dashboard.

---

## 📊 Usage Guide

### Analyzing Traffic

1. Input custom values for **Packet Size (Bytes)** and **Session Duration (ms)**.
2. Click **Analyze Traffic**.
3. The backend container processes the vector, appends it asynchronously to `traffic_logs.csv` inside the container, and returns the threat verdict (`SAFE` / `DANGER`) along with an anomaly score.

### Continuous Model Evolution

1. Submit at least **10 different traffic queries** to build a comprehensive baseline log history.
2. Scroll down to the **SOC Administration** section.
3. Click **🔄 Retrain AI Model**.
4. The containerized backend will dynamically fit a new Isolation Forest model on the live production log history, serialize it, and hot-swap it in memory with **zero downtime**.

---

## 🛡️ API Specification

### `POST /analyze/`

Evaluates a single network packet log vector.

* **Payload:**
```json
{
  "packet_size_bytes": 500.0,
  "session_duration_ms": 30.0
}

```


* **Response (Safe Traffic):**
```json
{
  "status": "SAFE",
  "threat_detected": false,
  "anomaly_score": 0.4215,
  "received_data": { "packet_size_bytes": 500.0, "session_duration_ms": 30.0 }
}

```



### `POST /retrain/`

Triggers an in-memory hot-swap model update based on gathered CSV logs.

* **Response (Success):**
```json
{
  "status": "success",
  "message": "AI successfully retrained on 14 real network logs!"
}
```