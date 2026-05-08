import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# -----------------------------
# SAMPLE TRAINING DATA
# -----------------------------
X = np.array([
    [95, 70, 16, 0.2, 25],
    [85, 90, 22, 0.8, 35],
    [92, 75, 18, 0.4, 28],
    [88, 85, 20, 0.6, 32],
    [97, 65, 14, 0.1, 23],
])

y = np.array([0, 1, 0, 1, 0])  # 0 = low risk, 1 = high risk

# -----------------------------
# SCALE DATA
# -----------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# TRAIN MODEL (ANN-like)
# -----------------------------
model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000)
model.fit(X_scaled, y)

# -----------------------------
# SAVE MODEL + SCALER
# -----------------------------
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("DONE: model and scaler saved")