# fast_audit.py
import socket
import requests
import json
from urllib.parse import urlparse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from shieldai_logs.brain_logo import draw_brain_logo  # <-- logo importado

# ------------------------------
# Logging explicativo
# ------------------------------
def log_info(msg):
    print(f"[INFO] {msg}")

def log_scan(msg):
    print(f"[SCAN] {msg}")

def log_result(msg):
    print(f"[RESULT] {msg}")

def log_warn(msg):
    print(f"[WARN] {msg}")

# ------------------------------
# Escaneo de puertos
# ------------------------------
def scan_ports(host, ports=[22, 80, 443]):
    results = {}
    log_info(f"Iniciando escaneo de puertos en {host}...")
    for port in ports:
        log_scan(f"Chequeando puerto {port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((host, port))
            results[port] = "ABIERTO"
            log_result(f"Puerto {port}: ABIERTO")
        except:
            results[port] = "CERRADO"
            log_result(f"Puerto {port}: CERRADO")
        finally:
            sock.close()
    return results

# ------------------------------
# Chequeo HTTP básico
# ------------------------------
def check_http(url):
    log_info(f"Chequeando HTTP en {url}...")
    try:
        resp = requests.head(url, timeout=3)
        headers = {k: v for k, v in resp.headers.items()}
        log_result(f"Status: {resp.status_code} {resp.reason}")
        for k, v in headers.items():
            log_result(f"{k}: {v}")
        if "X-Frame-Options" not in headers:
            log_warn("X-Frame-Options no configurado")
        return {"status": resp.status_code, "headers": headers}
    except Exception as e:
        log_warn(f"No se pudo conectar a {url}: {e}")
        return {"status": None, "headers": {}}

# ------------------------------
# Prueba XSS básica
# ------------------------------
def test_xss(url, params=None):
    if params is None:
        params = {"test": "<script>alert(1)</script>"}
    log_info(f"Probando XSS en {url} con parámetros {params}...")
    try:
        resp = requests.get(url, params=params, timeout=3)
        if "<script>alert(1)</script>" in resp.text:
            log_warn("Posible XSS detectado!")
            return True
        else:
            log_result("No se detectaron vulnerabilidades XSS.")
            return False
    except Exception as e:
        log_warn(f"No se pudo probar XSS: {e}")
        return False

# ------------------------------
# Generación de PDF
# ------------------------------
def generate_report(host, port_results, http_results, xss_detected, output_pdf="fast_audit_report.pdf"):
    log_info(f"Generando informe PDF: {output_pdf}...")
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Logo minimalista
    draw_brain_logo(c, x=40, y=750, size=50)

    w, h = A4
    margin = 40
    y = h - margin

    def line(text, size=11, move=14, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(margin, y, text)
        y -= move

    line(f"FastAudit - Informe de Escaneo para {host}", size=16, move=20, bold=True)
    line(f"Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", size=10, move=16)
    line("", move=10)

    line("1) Resultados de escaneo de puertos:", bold=True)
    for port, status in port_results.items():
        line(f"   - Puerto {port}: {status}")
    line("", move=10)

    line("2) Resultados de chequeo HTTP:", bold=True)
    line(f"   Status code: {http_results['status']}")
    for k, v in http_results["headers"].items():
        line(f"   {k}: {v}")
    line("", move=10)

    line("3) Resultados de pruebas XSS:", bold=True)
    line(f"   Posible vulnerabilidad XSS detectada: {xss_detected}")

    c.save()
    log_info("Informe PDF generado correctamente.")

# ------------------------------
# Función principal
# ------------------------------
def fast_audit(host_or_url):
    log_info("=== Iniciando FastAudit ===")
    log_info("Escaneo seguro activado por defecto")
    log_info("Cada paso será explicado con detalles")

    parsed = urlparse(host_or_url)
    host = parsed.netloc if parsed.netloc else host_or_url
    url = host_or_url if parsed.scheme else f"http://{host}"

    port_results = scan_ports(host)
    http_results = check_http(url)
    xss_detected = test_xss(url)

    generate_report(host, port_results, http_results, xss_detected)

    # Export JSON
    results_json = {
        "host": host,
        "ports": port_results,
        "http_headers": http_results["headers"],
        "http_status": http_results["status"],
        "xss_detected": xss_detected,
        "report_pdf": "fast_audit_report.pdf"
    }
    with open("fast_audit_results.json", "w") as f:
        json.dump(results_json, f, indent=4)
    log_info("Resultados exportados a fast_audit_results.json")
    log_info("=== FastAudit finalizado ===")

# ------------------------------
# Ejecución directa
# ------------------------------
if __name__ == "__main__":
    target = input("Introduce host o URL a escanear: ")
    fast_audit(target)
