# ShieldAI Logs 🚀

Librería y herramienta de IA para análisis de logs y auditoría de seguridad ligera.

## ✨ Funcionalidades
- Análisis de logs (fallos de login, errores críticos, accesos sospechosos).
- Detección de anomalías con IA (IsolationForest).
- Generación de informes PDF automáticos.
- Auditoría rápida para PYMES (`fast_audit.py`):
  - Escaneo de puertos TCP comunes
  - Chequeos HTTP (status, headers)
  - Prueba simple de XSS reflejado
- Auditoría extendida para empresas (`enterprise_audit.py`):
  - Verificación de SSL/TLS
  - Chequeo de cabeceras de seguridad HTTP

## 🔧 Instalación
```bash
git clone https://github.com/irene_java28/shieldai_logs
cd shieldai_logs
pip install -e .
