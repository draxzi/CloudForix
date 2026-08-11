# Security Policy — Cloud Forix

## Authorized Use Only

Cloud Forix is a digital forensics tool intended exclusively for **authorized forensic investigations**.

Use of this tool against any system, account, or data without **explicit written authorization** from the system owner is:

- A violation of this project's terms
- Potentially a criminal offence under computer access laws in your jurisdiction (e.g., Computer Fraud and Abuse Act (USA), Computer Misuse Act (UK), IT Act (India), and equivalent laws elsewhere)

---

## Supported Versions

| Version | Supported |
|---|---|
| Current (main) | ✅ Yes |

---

## Reporting a Security Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

If you discover a security vulnerability in Cloud Forix, please report it privately:

1. Email the maintainer directly (contact via GitHub profile)
2. Include in your report:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

You will receive a response within **7 days**. We will work to address valid vulnerabilities promptly.

---

## Credential and Secret Handling

This project **must never** have real credentials committed to version control, even to a private repository.

### Files that must never be committed:
- `credentials.json` — Google OAuth2 client secrets
- `token.json` — Google OAuth2 access/refresh tokens
- `.env` — environment variables with real values
- `keys/*.key` — Fernet encryption keys
- Any file containing API keys, passwords, or tokens

### Current State
The source files in this project contain credential references that should be loaded from environment variables. See `.env.example` for the required variable names.

If you find real credentials in any committed file, please report it immediately (see above).

---

## Forensic Data Handling

All collected forensic evidence, logs, and reports must be:

- **Stored securely** — access restricted to authorized investigators only
- **Encrypted at rest** — the tool provides Fernet encryption; ensure decryption keys are protected
- **Transmitted securely** — do not send evidence over unencrypted channels
- **Handled lawfully** — comply with applicable data protection regulations (GDPR, PDPA, etc.)
- **Deleted appropriately** — when investigation concludes, handle data per your organization's retention policy

---

## Basic Security Practices for Operators

1. Run the tool in an isolated investigation environment, not on a production machine
2. Use strong, unique investigator passwords for each case
3. Store encryption keys separately from encrypted evidence
4. Rotate all API credentials after each investigation case
5. Review all collected data before sharing reports — ensure no unrelated personal data is included
6. Keep Python dependencies updated: `pip list --outdated`

---

## Disclaimer

This tool is provided **as-is** for academic and research purposes. The authors make no warranties regarding its fitness for operational forensic investigations. Always consult qualified legal and forensic professionals for actual investigations.
