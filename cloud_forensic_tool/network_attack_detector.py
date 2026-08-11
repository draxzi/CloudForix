import psutil
import time
import requests
import os

# Trusted IPs (whitelist)
TRUSTED_IPS = ["13.107.137.11", "8.8.8.8", "1.1.1.1"]

# Known malicious IP blacklist
BLACKLIST_IPS = [
    "45.33.32.156",
    "103.21.244.0",
    "185.220.101.1"
]

# Suspicious ports
SUSPICIOUS_PORTS = [4444, 5555, 6666, 1337, 1234]

# Track connection frequency
connection_counter = {}

def get_ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        return f"{data.get('country')} - {data.get('city')}"
    except:
        return "Unknown Location"


def detect_suspicious_connections():
    alerts = []
    connections = psutil.net_connections()

    # Data transfer monitoring
    net_io_start = psutil.net_io_counters()
    time.sleep(1)
    net_io_end = psutil.net_io_counters()

    data_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
    data_recv = net_io_end.bytes_recv - net_io_start.bytes_recv

    for conn in connections:
        if conn.status == 'ESTABLISHED' and conn.raddr:
            ip = conn.raddr.ip
            port = conn.raddr.port

            # Ignore trusted IPs
            if ip in TRUSTED_IPS:
                continue

            # Ignore private IPs
            if ip.startswith(("192.168", "10.", "172.16", "127.0.0.1")):
                continue

            # Suspicious external IP
            alerts.append(f"Suspicious External Connection: {ip}:{port}")

            # IP Geolocation
            location = get_ip_geolocation(ip)
            alerts.append(f"IP Location: {ip} -> {location}")

            # Blacklist check
            if ip in BLACKLIST_IPS:
                alerts.append(f"Blacklisted IP Detected: {ip}")

            # Suspicious port check
            if port in SUSPICIOUS_PORTS:
                alerts.append(f"Backdoor Port Detected: {ip}:{port}")

            # Connection frequency detection
            if ip not in connection_counter:
                connection_counter[ip] = 1
            else:
                connection_counter[ip] += 1

            if connection_counter[ip] > 5:
                alerts.append(f"High Connection Frequency Detected from IP: {ip}")

    # Data exfiltration detection
    if data_sent > 10000000 or data_recv > 10000000:
        alerts.append("High Data Transfer Detected (Possible Data Exfiltration)")

    # DNS suspicious domain detection
    try:
        if os.path.exists("logs/dns_logs.txt"):
            with open("logs/dns_logs.txt", "r") as f:
                dns_logs = f.read()
                suspicious_domains = ["malware.com", "phishing.com", "badsite.net"]
                for domain in suspicious_domains:
                    if domain in dns_logs:
                        alerts.append(f"Suspicious Domain Access Detected: {domain}")
    except:
        pass

    return alerts