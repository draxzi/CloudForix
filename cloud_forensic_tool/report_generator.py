import os
from datetime import datetime

def generate_report(investigator, evidence_list, hash_list, integrity_list, ip_list, alerts, email_list, activity_list, timestamp_list):
    
    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_file = "reports/Final_Report_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"

    with open(report_file, "w") as report:
        report.write("=========== CLOUD FORENSIC INVESTIGATION REPORT ===========\n\n")

        report.write("Investigator Name: " + investigator + "\n")
        report.write("Report Date: " + str(datetime.now()) + "\n\n")

        report.write("Collected Evidence Files:\n")
        for file in evidence_list:
            report.write("- " + file + "\n")

        report.write("\nHash Values:\n")
        for h in hash_list:
            report.write(h + "\n")

        report.write("\nIntegrity Status:\n")
        for status in integrity_list:
            report.write(status + "\n")

        report.write("\n========== METADATA ==========\n")

        report.write("\nIP Addresses Found:\n")
        for ip in set(ip_list):
            report.write(ip + "\n")

        report.write("\nUser Emails Found:\n")
        for email in set(email_list):
            report.write(email + "\n")

        report.write("\nActivities Detected:\n")
        for act in set(activity_list):
            report.write(act + "\n")

        report.write("\nTimestamps Found:\n")
        for t in set(timestamp_list):
            report.write(t + "\n")

        report.write("\n========== SECURITY ALERTS ==========\n")
        if alerts:
            for alert in alerts:
                report.write("- " + alert + "\n")
        else:
            report.write("No suspicious activity detected\n")

        report.write("\n========== NETWORK ANALYSIS ==========\n")

        suspicious_ips = []
        if alerts:
            for alert in alerts:
                if "Suspicious External Connection" in alert:
                    ip = alert.split(":")[1].strip()
                    suspicious_ips.append(ip)

            report.write("Total Suspicious Connections: " + str(len(suspicious_ips)) + "\n")

            if len(suspicious_ips) > 5:
                report.write("Possible DDoS Attack Detected\n")

            if any("Blacklisted IP" in a for a in alerts):
                report.write("Blacklisted IP Communication Detected\n")

            if any("Backdoor Port" in a for a in alerts):
                report.write("Backdoor Access Detected\n")

            if any("High Data Transfer" in a for a in alerts):
                report.write("Possible Data Exfiltration Detected\n")

            report.write("Suspicious IP List:\n")
            for ip in set(suspicious_ips):
                report.write(ip + "\n")
        else:
            report.write("No suspicious network activity detected\n")

    print("\nFinal Report Generated:", report_file)