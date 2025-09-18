from shieldai_logs.fast_audit import fast_audit
from shieldai_logs.enterprise_audit import enterprise_audit
from shieldai_logs.analyzer import analyze_logs

def main():
    host_demo = "http://example.com"
    print("=== DEMO AUTOMÁTICA ShieldAI Logs ===\n")
    
    print(">>> Ejecutando FastAudit...\n")
    fast_audit(host_demo)
    
    print("\n>>> Ejecutando EnterpriseAudit...\n")
    enterprise_audit(host_demo)
    
    # Demo analyzer
    file_demo = "server-log.txt"
    results = analyze_logs(file_demo)
    print(f"\nResultados de análisis de logs:\n{results}")

if __name__ == "__main__":
    main()
