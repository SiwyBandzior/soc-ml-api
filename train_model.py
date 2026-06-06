import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

print("⏳ Generating synthetic network logs (normal traffic)...")

X_train = np.random.normal(loc=[500, 30], scale=[50, 5], size=(1000, 2))

print("🧠 Training the Isolation Forest model...")

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)

print("💾 Saving the 'brain' to a file...")
joblib.dump(model, 'anomaly_model.pkl')
print("✅ Success! The 'anomaly_model.pkl' file is ready." )