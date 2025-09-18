# shieldai_logs/reporter.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_report(file_path, analyzer_result, predictor_result,
                    output_pdf="report.pdf", company="", email=""):
    """
    Genera un PDF con resultados de ShieldAI Logs.
    Incluye: alertas, puntaje de riesgo y anomalías IA.
    """
    c = canvas.Canvas(output_pdf, pagesize=A4)
    w, h = A4
    margin = 40
    y = h - margin

    def line(text, size=11, move=14):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(margin, y, text)
        y -= move

    # Encabezado
    line("ShieldAI Logs - Informe de Seguridad", size=16, move=20)
    line(f"Archivo Analizado: {file_path}", size=11)
    line(f"Fecha: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", size=9, move=18)

    if company:
        line(f"Empresa: {company}", size=11)
    if email:
        line(f"Email: {email}", size=11)

    # Alertas
    line("1) Alertas detectadas:", size=12, move=16)
    alerts = analyzer_result.get("alerts", [])
    if alerts:
        for a in alerts:
            line(f"- Línea {a['line']} [{a['type']}]: {a['content']}", size=9, move=12)
    else:
        line("- No se detectaron alertas importantes", size=10)

    # Puntaje de riesgo
    line("", move=6)
    line(
        f"Puntaje de riesgo: {analyzer_result.get('risk_score', 0)} "
        f"/ {analyzer_result.get('total_lines', 0)}",
        size=11
    )

    # Anomalías IA
    line("", move=6)
    line(f"Score de anomalías IA: {predictor_result.get('anomaly_score', 0)}%", size=11)

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    footer_text = "ShieldAI Logs - Librería IA de ciberseguridad. Autor: Irene Vaquerizo"
    c.drawString(margin, 30, footer_text)

    c.save()
