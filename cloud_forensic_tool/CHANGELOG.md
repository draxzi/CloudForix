# Changelog

All notable changes to Cloud Forix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-08-11

### Initial Release — Cloud Forix

First public release of the Cloud Forix cloud forensic investigation tool.

#### Added

**Core Investigation Pipeline**
- `main.py` — Full investigation orchestrator: log collection → evidence processing → threat detection → report generation
- Interactive investigator name and password prompt at startup

**Log Collectors**
- `network_log_collector.py` — Collects active network connections (`netstat`), ARP table, and routing table
- `system_log_collector.py` — Reads Windows Security Event Log events for login (4624/4625), account (4720/4726), and process creation (4688) events
- `ems_web_collector.py` — Selenium-based EMS campus portal log collection (dashboard, fee page, timetable)
- `google_cloud_logs.py` — Google Drive file listing via Google Drive API v3
- `onedrive_logs.py` — OneDrive file listing via Microsoft Graph API
- `azure_ad_logs_collector.py` — Azure Active Directory sign-in logs via Microsoft Graph API
- `mde_collector.py` — Microsoft Defender for Endpoint security alerts via Microsoft Graph API
- `DNS_log_collector.py` — DNS log collection
- `ms_graphs_log.py` — Microsoft Graph sign-in logs and OneDrive activity
- `cloud_storage_api.py` — Cloud storage API utilities
- `multi_cloud_collector.py` — Multi-cloud collection coordinator

**Evidence Processing**
- `hash_module.py` — SHA-256 cryptographic hash generation for evidence files
- `encryption_module.py` — Fernet (AES-128-CBC) encryption and decryption of evidence files
- `key_manager.py` — Password-derived Fernet key generation using SHA-256 + Base64 encoding
- `blockchain_api.py` — Local JSON-based blockchain for chain of custody; SHA-256 linked blocks
- `chain_of_custody.py` — Chain of custody utilities
- `integrity_verifier.py` — Evidence integrity re-verification against blockchain records
- `metadata_extractor.py` — Regex-based extraction of IP addresses, emails, timestamps, login events, and activity keywords from log content
- `access_logger.py` — Investigator access audit logging

**Threat Detection**
- `malware_detector.py` — Running process scanning against keyword patterns + VirusTotal API hash lookup
- `virustotal_checker.py` — VirusTotal API v3 integration for file hash reputation lookup
- `unauthorized_access_detector.py` — Anomalous login detection in system logs
- `network_attack_detector.py` — Detection of suspicious external connections, blacklisted IPs, backdoor ports (4444, 5555, 6666, 1337, 1234), high connection frequency, data exfiltration, and suspicious DNS domains; IP geolocation via ip-api.com
- `attack_detector.py` — General attack detection utilities
- `realtime_monitor.py` — Background real-time monitoring thread

**Alerts & Reporting**
- `email_alert.py` — SMTP-based email alerting via Gmail when threats are detected
- `report_generator.py` — Timestamped plain-text final investigation report covering evidence, hashes, integrity, metadata, alerts, and network analysis
- `database.py` — SQLite database with `evidence`, `hashes`, and `alerts` tables

**Project Documentation**
- `README.md` — Comprehensive project documentation
- `LICENSE` — MIT License
- `.gitignore` — Python + forensic tool exclusion rules
- `.env.example` — Environment variable template
- `CONTRIBUTING.md` — Contribution guidelines
- `SECURITY.md` — Security policy and responsible disclosure
- `CODE_OF_CONDUCT.md` — Contributor Covenant Code of Conduct
- `CHANGELOG.md` — This file
- `requirements.txt` — Python dependency list

---

## [Unreleased]

Planned for future releases:
- Credential loading from environment variables (replacing hardcoded values)
- AWS CloudTrail log collection
- Automated Azure token refresh via MSAL
- Web-based investigation dashboard
- PDF report generation
- Unit and integration test suite
- Docker support
