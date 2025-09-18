import re
import json
from collections import Counter

# Ruta del log
LOG_FILE = "server-log.txt"
OUTPUT_JSON = "log_summary.json"

# Patrón para detectar intentos fallidos
FAILED_PATTERN = re.compile(
    r"Failed password for user (\S+) from (\d+\.\d+\.\d+\.\d+)"
)

alerts = []
ip_counter = Counter()

try:
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, start=1):
        match = FAILED_PATTERN.search(line)
        if match:
            user, ip = match.groups()
            alerts.append({
                "line": i,
                "type": "LoginFail",
                "user": user,
                "ip": ip,
                "content": line.strip()
            })
            ip_counter[ip] += 1

    # Calcular puntaje de riesgo: 5 puntos por intento fallido
    risk_score = len(alerts) * 5

    summary = {
        "alerts": alerts,
        "risk_score": risk_score,
        "total_lines": len(lines),
        "top_ips": ip_counter.most_common(5)  # Top 5 IPs con más fallos
    }

    # Guardar JSON
    with open(OUTPUT_JSON, "w") as out_file:
        json.dump(summary, out_file, indent=4)

    print(f"Resumen generado correctamente en {OUTPUT_JSON}")
    print(json.dumps(summary, indent=4))

except FileNotFoundError:
    print(f"[ERROR] No se encontró el archivo {LOG_FILE}")
