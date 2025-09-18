# enterprise_audit.py
import socket
import requests
import ssl
import json
from urllib.parse import urlparse
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from shieldai_logs.brain_logo import draw_brain_logo

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
def scan_ports(host, ports=[22, 80, 443, 8080]):
    results = {}
    log_info(f"Iniciando escaneo de puertos TCP comunes en {host}...")
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
# Chequeo HTTP headers de seguridad
# ------------------------------
SECURE_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy"
]

def check_http_security(url):
    log_info(f"Chequeando HTTP y headers de seguridad en {url}...")
    try:
        resp = requests.head(url, timeout=5)
        headers = {k: v for k, v in resp.headers.items()}
        log_result(f"Status: {resp.status_code} {resp.reason}")
        for header in SECURE_HEADERS:
            if header not in headers:
                log_warn(f"Header de seguridad faltante: {header}")
            else:
                log_result(f"{header}: {headers[header]}")
        return {"status": resp.status_code, "headers": headers}
    except Exception as e:
        log_warn(f"No se pudo conectar a {url}: {e}")
        return {"status": None, "headers": {}}

# ------------------------------
# SSL/TLS básico
# ------------------------------
def check_ssl(host):
    log_info(f"Comprobando certificado SSL/TLS en {host}...")
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, 443), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                log_result(f"Certificado válido hasta: {cert['notAfter']}")
                log_result(f"Emisor: {cert['issuer']}")
                return cert
    except Exception as e:
        log_warn(f"Error SSL/TLS: {e}")
        return None

# ------------------------------
# Generación PDF
# ------------------------------
def generate_report(host, port_results, http_results, ssl_cert, output_pdf="enterprise_audit_report.pdf"):
    log_info(f"Generando informe PDF: {output_pdf}...")
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Dibuja el logo minimalista en la esquina superior izquierda
    draw_brain_logo(c, x=40, y=750, size=50)

    w, h = A4
    margin = 40
    y = h - margin

    def line(text="", size=11, move=14, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(margin, y, text)
        y -= move

    line(f"EnterpriseAudit - Informe de Escaneo para {host}", size=16, move=20, bold=True)
    line(f"Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", size=10, move=16)
    line("", move=10)

    line("1) Resultados de escaneo de puertos:", bold=True)
    for port, status in port_results.items():
        line(f"   - Puerto {port}: {status}")
    line("", move=10)

    line("2) Resultados de chequeo HTTP y headers de seguridad:", bold=True)
    line(f"   Status code: {http_results['status']}")
    for k, v in http_results["headers"].items():
        line(f"   {k}: {v}")
    line("", move=10)

    line("3) Resultados SSL/TLS:", bold=True)
    if ssl_cert:
        line(f"   Válido hasta: {ssl_cert.get('notAfter', 'desconocido')}")
        line(f"   Emisor: {ssl_cert.get('issuer', 'desconocido')}")
    else:
        line("   No se pudo verificar SSL/TLS")

    line("", move=20)
    line("Resumen:", bold=True)
    line("Auditoría completa para PyMEs que necesitan revisión seria y profesional.")
    line("Incluye PDF y JSON de resultados para integración o informes corporativos.")

    c.save()
    log_info("Informe PDF generado correctamente.")

# ------------------------------
# Función principal
# ------------------------------
def enterprise_audit(host_or_url):
    log_info("=== Iniciando EnterpriseAudit ===")
    log_info("Modo muy seguro activado por defecto")
    parsed = urlparse(host_or_url)
    host = parsed.netloc if parsed.netloc else host_or_url
    url = host_or_url if parsed.scheme else f"https://{host}"

    port_results = scan_ports(host)
    http_results = check_http_security(url)
    ssl_cert = check_ssl(host)

    generate_report(host, port_results, http_results, ssl_cert)

    # Export JSON
    results_json = {
        "host": host,
        "ports": port_results,
        "http_headers": http_results["headers"],
        "http_status": http_results["status"],
        "ssl_cert": ssl_cert,
        "report_pdf": "enterprise_audit_report.pdf"
    }
    with open("enterprise_audit_results.json", "w") as f:
        json.dump(results_json, f, indent=4)
    log_info("Resultados exportados a enterprise_audit_results.json")
    log_info("=== EnterpriseAudit finalizado ===")

# ------------------------------
# Ejecución directa
# ------------------------------
if __name__ == "__main__":
    target = input("Introduce host o URL a escanear: ")
    enterprise_audit(target)
