# ☁️ Cloud Forix — Cloud Forensic Investigation Tool

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Academic%20Research-orange)](https://github.com/draxzi/CloudForix)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightblue?logo=windows)](https://github.com/draxzi/CloudForix)
[![Security](https://img.shields.io/badge/Security-Forensics%20Tool-red?logo=shield)](SECURITY.md)

> **Cloud Forix** is a Python-based cloud digital forensics investigation tool developed as an academic research project. It collects, encrypts, hashes, and analyses logs from multiple cloud platforms — Microsoft Azure, Microsoft 365 (OneDrive, MDE), Google Drive, local network, and system sources — while maintaining forensic chain of custody via a lightweight local blockchain.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflow](#workflow)
- [Security Context](#security-context)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Academic Context](#academic-context)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

Cloud Forix is a command-line forensic investigation tool designed for cloud environments. It automates the evidence collection pipeline — from multi-cloud log acquisition to encrypted storage, hash verification, threat detection, and final report generation — reducing manual investigator effort while maintaining forensic integrity.

The tool targets the increasingly common scenario where digital evidence is distributed across multiple cloud providers and enterprise services, making traditional single-platform forensic tools insufficient.

---

## Problem Statement

Modern cybercrime investigations frequently involve evidence spread across multiple cloud platforms (Microsoft Azure, Microsoft 365, Google Workspace), on-premises networks, and enterprise management systems. Investigators face:

- **Fragmented evidence** — different APIs, formats, and access methods per platform
- **Chain of custody gaps** — manual processes introduce risk of tampering allegations
- **Encryption gaps** — collected evidence often stored without proper protection
- **Detection delays** — manual log review is too slow for incident response

Cloud Forix addresses these gaps by providing an automated, unified collection and analysis pipeline with cryptographic integrity assurances.

---

## Features

| Feature | Description |
|---|---|
| **Multi-Cloud Log Collection** | Collects logs from Microsoft Azure AD, Microsoft Defender for Endpoint (MDE), OneDrive, Google Drive, EMS portal, local network, system events, and DNS |
| **Evidence Hashing** | SHA-256 cryptographic hash generated for every collected evidence file |
| **Blockchain Chain of Custody** | Local JSON-based blockchain records each evidence file hash, linking blocks via previous-hash pointers |
| **Evidence Encryption** | Collected log files encrypted using Fernet symmetric encryption (AES-128-CBC) derived from investigator password |
| **Integrity Verification** | Re-hashes and verifies evidence against blockchain records after storage |
| **Metadata Extraction** | Extracts IP addresses, email addresses, timestamps, and activity keywords from log content using regex |
| **Malware Detection** | Scans running system processes against keyword patterns and VirusTotal API for known-malicious file hashes |
| **Unauthorized Access Detection** | Detects anomalous login events in system logs |
| **Network Attack Detection** | Identifies suspicious external connections, blacklisted IPs, backdoor ports, high connection frequency, and potential data exfiltration |
| **Real-Time Monitoring** | Background thread monitors for new activity during an investigation session |
| **Email Alerting** | Sends alert emails via SMTP when threats are detected |
| **SQLite Database** | Stores evidence metadata, hashes, and alerts in a local forensic database |
| **Final Report Generation** | Generates a timestamped, structured investigation report in plain text |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLOUD FORIX                              │
│                  Cloud Forensic Investigation Tool              │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
   ┌──────▼──────┐    ┌───────▼──────┐   ┌────────▼──────┐
   │  Log         │    │  Evidence    │   │  Threat        │
   │  Collectors  │    │  Processing  │   │  Detection     │
   └──────┬──────┘    └───────┬──────┘   └────────┬──────┘
          │                   │                   │
   ┌──────▼──────────────────────────────────────▼──────┐
   │  Azure AD  │  OneDrive  │  MDE  │  Google Drive    │
   │  Network   │  System    │  EMS  │  DNS             │
   └─────────────────────────────────────────────────────┘
          │                   │
   ┌──────▼──────┐    ┌───────▼──────┐
   │  SHA-256    │    │  Fernet      │
   │  Hash       │    │  Encryption  │
   └──────┬──────┘    └───────┬──────┘
          │                   │
   ┌──────▼──────────────────▼──────┐
   │        Local Blockchain        │
   │    (Chain of Custody Ledger)   │
   └──────────────────┬─────────────┘
                      │
   ┌──────────────────▼─────────────┐
   │         SQLite Database        │
   │  (evidence / hashes / alerts)  │
   └──────────────────┬─────────────┘
                      │
   ┌──────────────────▼─────────────┐
   │      Final Investigation       │
   │      Report + Email Alert      │
   └────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.9+ |
| **Cloud APIs** | Microsoft Graph API, Google Drive API v3, Google Drive Activity API |
| **Authentication** | OAuth2 (Google), MSAL / Client Credentials (Azure) |
| **Encryption** | `cryptography` (Fernet / AES-128-CBC) |
| **Database** | SQLite via `sqlite3` |
| **Web Scraping** | Selenium + BeautifulSoup4 |
| **Threat Intel** | VirusTotal API v3 |
| **Process Monitoring** | `psutil` |
| **Network Analysis** | `psutil`, `netstat`, `arp`, ip-api.com geolocation |
| **Email** | `smtplib` + Gmail SMTP |
| **Blockchain** | Custom JSON-based chain (local, SHA-256 linked) |
| **Hashing** | SHA-256 (`hashlib`) |
| **System Logs** | `wevtutil` (Windows Event Log) |

---

## Project Structure

```
cloud_forensic_tool/
│
├── main.py                        # Entry point — orchestrates the full investigation pipeline
│
├── # ── Log Collectors ──────────────────────────────────────────
├── network_log_collector.py       # Captures active network connections, ARP, routing table
├── system_log_collector.py        # Reads Windows Security Event Log (login, account, process events)
├── ems_web_collector.py           # Selenium-based collector for EMS campus portal logs
├── google_cloud_logs.py           # Google Drive file activity via Google Drive API
├── onedrive_logs.py               # OneDrive file listing via Microsoft Graph API
├── azure_ad_logs_collector.py     # Azure AD sign-in logs via Microsoft Graph API
├── mde_collector.py               # Microsoft Defender for Endpoint alerts via Graph API
├── DNS_log_collector.py           # DNS log collection
├── ms_graphs_log.py               # Microsoft Graph sign-in + OneDrive activity collector
├── cloud_storage_api.py           # Cloud storage API utilities
├── multi_cloud_collector.py       # Multi-cloud collection coordinator
│
├── # ── Evidence Processing ──────────────────────────────────────
├── hash_module.py                 # SHA-256 hash generation
├── encryption_module.py           # Fernet encryption/decryption of evidence files
├── key_manager.py                 # Derives Fernet key from investigator password
├── blockchain_api.py              # Appends evidence hash to local blockchain ledger
├── chain_of_custody.py            # Chain of custody utilities
├── integrity_verifier.py          # Re-verifies evidence hash against blockchain
├── metadata_extractor.py          # Extracts IPs, emails, timestamps, activities from logs
│
├── # ── Detection Modules ────────────────────────────────────────
├── malware_detector.py            # Process scanning + VirusTotal API hash lookup
├── virustotal_checker.py          # VirusTotal API integration
├── unauthorized_access_detector.py # Detects anomalous logins
├── network_attack_detector.py     # Suspicious connections, blacklist, port, DDoS detection
├── attack_detector.py             # General attack detection utilities
├── realtime_monitor.py            # Background real-time monitoring thread
│
├── # ── Alerts & Reports ─────────────────────────────────────────
├── email_alert.py                 # SMTP email alert dispatch
├── report_generator.py            # Final investigation report generator
├── access_logger.py               # Investigator access audit logger
│
├── # ── Data Storage ─────────────────────────────────────────────
├── database.py                    # SQLite database — evidence, hashes, alerts tables
├── get_graph_token.py             # Microsoft Graph token acquisition utility
│
├── # ── Runtime Directories (git-ignored) ───────────────────────
├── logs/                          # Collected raw log files (runtime, excluded from git)
├── evidence/                      # Encrypted evidence files (runtime, excluded from git)
├── blockchain/                    # Local blockchain JSON (runtime, excluded from git)
├── reports/                       # Generated investigation reports (runtime, excluded from git)
├── keys/                          # Encryption key files (excluded from git)
├── temp/                          # Temporary working files (excluded from git)
│
├── # ── Configuration ────────────────────────────────────────────
├── .env.example                   # Environment variable template (safe to commit)
├── .gitignore                     # Git exclusion rules
└── requirements.txt               # Python dependencies
```

---

## Installation

### Requirements

- **Python 3.9+**
- **Windows OS** (system log collection uses `wevtutil`; network uses `netstat`)
- **Google Chrome** + matching **ChromeDriver** (for EMS Selenium collector)
- Cloud API credentials (see [Configuration](#configuration))

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/draxzi/CloudForix.git
cd CloudForix/cloud_forensic_tool

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp .env.example .env
# Edit .env with your real API keys and credentials
```

---

## Configuration

### Google Drive API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → Enable **Drive API** and **Drive Activity API**
3. Create **OAuth 2.0 Client ID** (Desktop app type)
4. Download the credentials JSON and save as `credentials.json` in the project directory

### Microsoft Azure (Graph API)

1. Go to [Azure Active Directory](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade)
2. Register a new application → note **Tenant ID**, **Client ID**
3. Create a **Client Secret** → note the value
4. Assign required Graph API permissions:
   - `AuditLog.Read.All`
   - `SecurityEvents.Read.All`
   - `Files.Read.All`
   - `User.Read.All`

### VirusTotal

1. Create a free account at [VirusTotal](https://www.virustotal.com)
2. Copy your API key from account settings

### Email Alerts (Gmail)

1. Enable **2-Step Verification** on the Gmail account
2. Generate an **App Password** ([instructions](https://support.google.com/accounts/answer/185833))
3. Use the app password (not your main password) as `SENDER_PASSWORD`

### Environment Variables

Set all values in `.env` (copy from `.env.example`):

```env
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
AZURE_TENANT_ID=...
AZURE_CLIENT_ID=...
AZURE_CLIENT_SECRET=...
VIRUSTOTAL_API_KEY=...
SENDER_EMAIL=...
SENDER_PASSWORD=...
RECEIVER_EMAIL=...
```

> **Note:** The current source files use hardcoded credential placeholders for development. In production use, load credentials from environment variables or a secrets manager. Do **not** commit real credentials to version control.

---

## Usage

```bash
# Run the full investigation pipeline
python main.py
```

You will be prompted for:

1. **Investigator Name** — recorded in chain of custody and report
2. **Investigator Password** — used to derive the Fernet encryption key for evidence files

The tool will then:
- Start real-time background monitoring
- Collect logs from all configured cloud sources
- Process, hash, encrypt, and blockchain-record each evidence file
- Run threat detection
- Send email alerts (if threats found)
- Generate a final investigation report in `reports/`

---

## Workflow

```
Start
  │
  ├─ Enter investigator name
  ├─ Enter investigator password (for encryption key)
  │
  ├─ Initialize SQLite database
  ├─ Start real-time monitor (background thread)
  │
  ├─ COLLECT LOGS
  │   ├─ Network logs (netstat / ARP / route)
  │   ├─ System logs (Windows Event Log)
  │   ├─ EMS portal logs (Selenium)
  │   ├─ Google Drive logs (Drive API)
  │   ├─ OneDrive logs (Graph API)
  │   ├─ Azure AD sign-in logs (Graph API)
  │   ├─ MDE security alerts (Graph API)
  │   └─ DNS logs
  │
  ├─ PROCESS EACH LOG FILE
  │   ├─ Extract metadata (IPs, emails, timestamps, activities)
  │   ├─ Generate SHA-256 hash
  │   ├─ Store hash in local blockchain
  │   ├─ Store evidence record in SQLite
  │   ├─ Encrypt file (Fernet)
  │   └─ Verify integrity (hash re-check against blockchain)
  │
  ├─ THREAT DETECTION
  │   ├─ Malware detection (process scan + VirusTotal)
  │   ├─ Unauthorized access detection
  │   └─ Network attack detection
  │
  ├─ Send email alerts (if threats detected)
  │
  ├─ Generate Final Investigation Report
  │
  └─ Investigation Complete
```

---

## Security Context

This tool is designed for **authorized forensic investigations only**. Investigators using this tool must:

- Have **explicit written authorization** before collecting logs from any system or service
- Comply with applicable laws including computer access laws, data protection regulations (GDPR, PDPA, etc.), and institutional policies
- Treat all collected forensic data as confidential and store it securely
- Not share evidence files, decryption keys, or API credentials with unauthorized parties

See [SECURITY.md](SECURITY.md) for the full security policy.

---

## Limitations

- **Windows-only** — system log collection uses `wevtutil` and `netstat` (Windows)
- **EMS collector** — requires manual login interaction (60-second window)
- **Hardcoded credentials** — current version stores credentials in source files; production use should migrate to environment variables or a secrets manager
- **Local blockchain** — the blockchain is a local JSON file, not a distributed ledger; it provides tamper-evidence within the local system but not across systems
- **API token expiry** — Azure Bearer tokens are short-lived; the tool does not auto-refresh them
- **VirusTotal rate limits** — the free API key has rate limits that may slow malware scanning

---

## Future Improvements

- [ ] Migrate all credentials to environment variables / dotenv loading
- [ ] Add AWS CloudTrail log collection
- [ ] Web-based dashboard (Flask/Django) for investigation management
- [ ] Automated Azure token refresh using MSAL
- [ ] Distributed blockchain for multi-investigator environments
- [ ] Support for Linux and macOS system log collection
- [ ] Docker containerization for portable deployment
- [ ] Unit and integration tests
- [ ] PDF report generation
- [ ] SIEM integration (Splunk / Elasticsearch)

---

## Academic Context

Cloud Forix was developed as an academic final-year project exploring cloud digital forensics methodologies. It demonstrates the practical implementation of:

- Multi-cloud log acquisition
- Cryptographic evidence integrity (SHA-256 + Fernet)
- Blockchain-based chain of custody
- Automated threat detection
- Forensic reporting

> **Note:** This is a research/academic prototype. It has not undergone security auditing for production deployment. Use in real investigations requires careful review of local laws, institutional policies, and operational security practices.

---

## Contributors

| Name | Role |
|---|---|
| **draxzi** | Lead Developer / Researcher |

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

> **⚠️ License Review Note:** This is currently a private academic project. The MIT license allows broad reuse. If this project is associated with institutional IP, patent considerations, or confidentiality requirements, the owner should review the license choice before making the repository public. Alternative options include a custom academic/non-commercial license.

---

## Acknowledgements

- [Google Drive API Documentation](https://developers.google.com/drive/api/v3/reference)
- [Microsoft Graph API Documentation](https://docs.microsoft.com/en-us/graph/overview)
- [VirusTotal API Documentation](https://developers.virustotal.com/reference)
- [cryptography library (PyCA)](https://cryptography.io)
- [psutil documentation](https://psutil.readthedocs.io)
- [Selenium WebDriver](https://www.selenium.dev)
