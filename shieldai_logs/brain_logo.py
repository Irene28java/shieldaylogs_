# brain_logo.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def draw_brain_logo(c, x=50, y=750, size=50):
    """
    Dibuja un cerebro minimalista blanco sobre azul eléctrico.
    x, y: posición en la página
    size: tamaño del logo
    """
    # Fondo azul eléctrico
    c.setFillColor(HexColor("#1E90FF"))  # azul eléctrico
    c.circle(x + size/2, y + size/2, size/2, fill=1)

    # Cerebro en blanco (simplificado como una forma ovalada con curvas)
    c.setFillColor("white")
    c.ellipse(x + 5, y + 10, x + size - 5, y + size - 10, fill=1)

if __name__ == "__main__":
    c = canvas.Canvas("logo_demo.pdf", pagesize=A4)
    draw_brain_logo(c)
    c.save()
