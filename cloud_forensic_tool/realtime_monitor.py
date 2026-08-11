import time
import psutil
from malware_detector import detect_malware
from unauthorized_access_detector import detect_unauthorized_access
from network_attack_detector import detect_suspicious_connections
from email_alert import send_email_alert

def start_realtime_monitor():
    print("Real-time monitoring started...")

    while True:
        alerts = []

        # Run detectors
        alerts.extend(detect_malware())
        alerts.extend(detect_unauthorized_access())
        alerts.extend(detect_suspicious_connections())

        # If alerts found → send email immediately
        if alerts:
            print("Real-time Alert Detected!")
            send_email_alert("\n".join(alerts))

        # Wait 30 seconds before next scan
        time.sleep(10)