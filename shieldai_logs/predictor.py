import numpy as np
from sklearn.ensemble import IsolationForest
from .utils import load_log

def predict_risk(file_path):
    """
    Predice riesgo de anomalías usando IsolationForest.
    Cada línea del log es un "evento".
    Vectoriza simple: longitud + cantidad de palabras.
    Retorna: { 'anomalies': [...], 'anomaly_score': valor }
    """
    lines = load_log(file_path)
    if isinstance(lines, dict) and "error" in lines:
        return lines

    # vectorización simple: [longitud, nº palabras]
    X = np.array([[len(l), len(l.split())] for l in lines])

    if len(X) < 5:
        return {"error": "Log demasiado corto para predicción"}

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    preds = model.predict(X)  # -1 anomalía, 1 normal

    anomalies = [
        {"line": i + 1, "content": lines[i].strip()}
        for i, p in enumerate(preds) if p == -1
    ]

    anomaly_score = len(anomalies) / len(lines) * 100

    return {"anomalies": anomalies, "anomaly_score": round(anomaly_score, 2)}
