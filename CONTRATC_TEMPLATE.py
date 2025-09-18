# generate_contract.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

def generate_contract_pdf(output="CONTRACT_TEMPLATE.pdf"):
    c = canvas.Canvas(output, pagesize=A4)
    w, h = A4
    margin = 40
    y = h - margin

    def line(text, size=11, move=16):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(margin, y, text)
        y -= move

    # Título
    line("CONTRATO DE SERVICIOS DE AUDITORÍA DE SEGURIDAD", size=16, move=24)
    line(f"Fecha de emisión: {date.today()}")
    line("")

    # Partes
    line("1) PARTES")
    line("Este contrato se celebra entre:")
    line("- Prestador de servicios: Irene Vaquerizo / ShieldAI Logs")
    line("- Cliente: ________________________________")
    line("")

    # Objeto
    line("2) OBJETO DEL CONTRATO")
    line("El presente contrato tiene por objeto la realización de pruebas de seguridad")
    line("y auditorías éticas autorizadas sobre sistemas del Cliente, usando herramientas")
    line("automatizadas y análisis de logs.")
    line("")

    # Alcance
    line("3) ALCANCE")
    line("- Activos: IPs, dominios y sistemas autorizados por el Cliente")
    line("- Pruebas permitidas: escaneo de puertos, análisis HTTP, pruebas XSS reflejado")
    line("- Exclusiones: explotación de vulnerabilidades, ataques destructivos, acceso a datos")
    line("")

    # Duración
    line("4) DURACIÓN Y CALENDARIO")
    line("El presente contrato será válido desde la fecha de aceptación hasta la finalización")
    line("de la auditoría, conforme al calendario acordado entre las partes.")
    line("")

    # Responsabilidades
    line("5) RESPONSABILIDADES")
    line("- Prestador: realizar pruebas de manera ética y responsable, respetando el alcance")
    line("- Cliente: proporcionar información precisa y autorización escrita")
    line("")

    # Confidencialidad
    line("6) CONFIDENCIALIDAD")
    line("Toda información del Cliente y hallazgos se mantendrán confidenciales, salvo autorización")
    line("expresa para divulgación.")
    line("")

    # Propiedad de resultados
    line("7) PROPIEDAD DE RESULTADOS")
    line("Los resultados, informes y hallazgos pertenecen al Cliente. El Prestador no los usará")
    line("para otros fines sin consentimiento.")
    line("")

    # Limitación de responsabilidad
    line("8) LIMITACIÓN DE RESPONSABILIDAD")
    line("El Prestador no se hace responsable de daños indirectos, pérdida de datos o incidentes")
    line("ocasionados por sistemas previamente vulnerables, siempre que haya actuado conforme al contrato.")
    line("")

    # Firma
    line("9) FIRMA Y ACEPTACIÓN")
    line("Cliente: ______________________  Fecha: _____________")
    line("Prestador: _____________________  Fecha: _____________")
    line("")

    c.save()

if __name__ == "__main__":
    generate_contract_pdf()
