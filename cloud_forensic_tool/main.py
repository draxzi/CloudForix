import os
import threading

# Evidence processing
from hash_module import generate_hash
from blockchain_api import store_hash
from encryption_module import encrypt_file
from integrity_verifier import verify_integrity
from metadata_extractor import extract_metadata

# Log collectors
from network_log_collector import collect_network_logs
from system_log_collector import collect_system_logs
from ems_web_collector import collect_ems_logs
from google_cloud_logs import collect_google_drive_logs
from onedrive_logs import collect_onedrive_logs
from azure_ad_logs_collector import collect_azure_logs
from mde_collector import collect_mde_logs
from DNS_log_collector import collect_dns_logs
# Detection modules
from malware_detector import detect_malware
from unauthorized_access_detector import detect_unauthorized_access
from network_attack_detector import detect_suspicious_connections
from access_logger import log_access

# Alerts and reports
from email_alert import send_email_alert
from report_generator import generate_report

# Database
from database import create_database, insert_evidence, insert_hash

# Real-time monitoring
from realtime_monitor import start_realtime_monitor


def run_tool():
    print("====================================")
    print("   CLOUD FORENSIC INVESTIGATION TOOL")
    print("====================================")

    investigator = input("Enter Investigator Name: ")

    # Lists for final report
    all_evidence = []
    all_hashes = []
    all_integrity = []
    all_ips = []
    all_emails = []
    all_activities = []
    all_timestamps = []
    all_alerts = []

    # Step 1: Create database
    create_database()

    # Step 2: Start real-time monitoring
    monitor_thread = threading.Thread(target=start_realtime_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    # Step 3: Collect logs
    print("\nCollecting logs...")
    net_log = collect_network_logs()
    sys_log = collect_system_logs()
    ems_log = collect_ems_logs()
    gdrive_log = collect_google_drive_logs()
    onedrive_log = collect_onedrive_logs()
    azure_log = collect_azure_logs()
    mde_log = collect_mde_logs()
    dns_log = collect_dns_logs()
    log_files = [net_log, sys_log, ems_log, gdrive_log, onedrive_log, azure_log, mde_log, dns_log]
    log_files.append(dns_log)
    # Step 4: Process evidence
    print("\nProcessing evidence...")
    for filepath in log_files:
        if filepath and os.path.exists(filepath):
            file = os.path.basename(filepath)
            print("Processing:", file)

            # Metadata extraction
            metadata = extract_metadata(filepath)
            all_ips.extend(metadata.get("ip_addresses", []))
            all_emails.extend(metadata.get("emails", []))
            all_activities.extend(metadata.get("activities", []))
            all_timestamps.extend(metadata.get("timestamps", []))

            # Hash
            file_hash = generate_hash(filepath)
            print("Hash Generated:", file_hash)

            # Store hash in blockchain
            store_hash(file, file_hash)

            # Store in database
            insert_evidence(file, filepath, "Cloud Log")
            insert_hash(file, file_hash)

            # Encrypt evidence
            encrypt_file(filepath)

            # Verify integrity
            integrity = verify_integrity(file, file_hash)
            print("Integrity Status:", integrity)

            # Integrity alert
            if integrity != "Verified":
                alert_msg = f"Integrity check failed for evidence: {file}"
                all_alerts.append(alert_msg)

            # Log investigator access
            log_access(file, investigator)

            # Store evidence info
            all_evidence.append(file)
            all_hashes.append(file_hash)
            all_integrity.append(integrity)

    # Step 5: Threat Detection
    print("\nRunning threat detection...")

    malware_alerts = detect_malware()
    print("Malware detection done")

    unauth_alerts = detect_unauthorized_access()
    print("Unauthorized access detection done")

    network_alerts = detect_suspicious_connections()
    all_alerts.extend(network_alerts)
    print("Network attack detection done")

    all_alerts.extend(malware_alerts)
    all_alerts.extend(unauth_alerts)
    all_alerts.extend(network_alerts)

    # Step 6: Send Email Alerts
    if all_alerts:
        print("\nSending email alert...")
        send_email_alert("\n".join(all_alerts))

    # Step 7: Generate Final Report
    generate_report(
        investigator,
        all_evidence,
        all_hashes,
        all_integrity,
        all_ips,
        all_alerts,
        all_emails,
        all_activities,
        all_timestamps
    )

    print("\n=== Investigation Completed Successfully ===")


if __name__ == "__main__":
    run_tool()