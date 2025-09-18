import re
from .utils import load_log

def analyze_logs(file_path):
    """
    Analiza un log simple de servidor y devuelve alertas.
    Detecta:
      - Intentos fallidos de login
      - Errores críticos
      - Escaladas de privilegios
    Retorna un diccionario con resultados y un puntaje de riesgo.
    """
    lines = load_log(file_path)
    if isinstance(lines, dict) and "error" in lines:
        return lines

    alerts = []
    risk_score = 0

    for i, line in enumerate(lines, 1):
        line_lower = line.lower()

        if re.search(r"failed password|authentication failure|invalid user", line_lower):
            alerts.append({"line": i, "type": "LoginFail", "content": line.strip()})
            risk_score += 5

        elif re.search(r"error|critical|segfault|panic", line_lower):
            alerts.append({"line": i, "type": "Error", "content": line.strip()})
            risk_score += 3

        elif re.search(r"sudo|root access", line_lower):
            alerts.append({"line": i, "type": "PrivEsc", "content": line.strip()})
            risk_score += 4

    return {"alerts": alerts, "risk_score": risk_score, "total_lines": len(lines)}
