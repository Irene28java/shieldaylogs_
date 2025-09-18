from shieldai_logs.analyzer import analyze_logs
from shieldai_logs.predictor import predict_risk
from shieldai_logs.reporter import generate_report

file_path = "server-log.log"  # asegúrate que el archivo exista

# Analizar logs y predecir riesgos
alerts = analyze_logs(file_path)
risk = predict_risk(file_path)

# Generar reporte PDF
generate_report(file_path, alerts, risk, output_pdf="reporte.pdf")

print("Informe generado con éxito")
