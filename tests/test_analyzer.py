# tests/test_analyzer.py
import os
import pytest
from shieldai_logs.analyzer import analyze_logs
from shieldai_logs.predictor import predict_risk
from shieldai_logs.reporter import generate_report

# Creamos un log de ejemplo temporal
SAMPLE_LOG = "sample_test.log"
PDF_OUTPUT = "test_report.pdf"

@pytest.fixture(scope="module")
def create_sample_log():
    log_lines = [
        "Jan 01 12:00:00 server sshd[1234]: Failed password for invalid user admin from 192.168.1.10 port 2222",
        "Jan 01 12:01:00 server sshd[1234]: Accepted password for root from 192.168.1.11 port 3333",
        "Jan 01 12:02:00 server application[5678]: critical error: something broke",
        "Jan 01 12:03:00 server sudo: root access granted for user test"
    ]
    with open(SAMPLE_LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    yield SAMPLE_LOG
    os.remove(SAMPLE_LOG)
    if os.path.exists(PDF_OUTPUT):
        os.remove(PDF_OUTPUT)

def test_analyze_logs(create_sample_log):
    result = analyze_logs(create_sample_log)
    assert "alerts" in result
    assert "risk_score" in result
    assert result["risk_score"] > 0
    assert len(result["alerts"]) > 0

def test_predict_risk(create_sample_log):
    result = predict_risk(create_sample_log)
    assert "anomalies" in result
    assert "anomaly_score" in result
    assert 0 <= result["anomaly_score"] <= 100

def test_generate_report(create_sample_log):
    analyzer_result = analyze_logs(create_sample_log)
    predictor_result = predict_risk(create_sample_log)
    generate_report(create_sample_log, analyzer_result, predictor_result, output_pdf=PDF_OUTPUT, company="TestCo", email="test@example.com")
    assert os.path.exists(PDF_OUTPUT)
