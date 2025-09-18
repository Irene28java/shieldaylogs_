# generate_consent.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date

def generate_consent_pdf(output="CONSENT_TEMPLATE.pdf"):
    c = canvas.Canvas(output, pagesize=A4)
    w, h = A4
    margin = 40
    y = h - margin

    def line(text, size=11, move=16):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(margin, y, text)
        y -= move

    line("AUTORIZACIÓN DE PRUEBAS DE SEGURIDAD", size=16, move=24)
    line(f"Fecha de emisión: {date.today()}")
    line("")
    line("Yo, ____________________________, representante autorizado de la empresa")
    line("_____________________________________, autorizo a:")
    line("Nombre / Empresa: ______________________________")
    line("Correo: ________________________________________")
    line("")
    line("Alcance autorizado:")
    line("- Escaneo de puertos TCP comunes")
    line("- Verificación de cabeceras HTTP y estado de respuesta")
    line("- Pruebas de XSS reflejado en parámetros GET")
    line("")
    line("Exclusiones:")
    line("- No explotación de vulnerabilidades")
    line("- No ataques de denegación de servicio")
    line("- No acceso a datos confidenciales")
    line("")
    line("Ventana autorizada: ____________________________")
    line("Contacto de soporte de la empresa durante la prueba:")
    line("Nombre: ____________________ Teléfono: ______________ Email: ______________")
    line("")
    line("Firma del responsable autorizado: ______________________")

    c.save()

if __name__ == "__main__":
    generate_consent_pdf()
