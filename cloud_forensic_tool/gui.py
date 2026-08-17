"""
Cloud Forix — Tkinter GUI
=========================
A graphical front-end for the Cloud Forix forensic investigation pipeline.

Launch:
    python gui.py

All forensic logic lives in the existing modules (main.py, collectors, etc.).
This file ONLY provides the GUI shell and threads; it never duplicates forensic logic.
"""

import os
import sys
import ctypes
import threading
import traceback
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
from datetime import datetime

# ── Make sure imports resolve from the same directory as gui.py ──────────────
GUI_DIR = os.path.dirname(os.path.abspath(__file__))
if GUI_DIR not in sys.path:
    sys.path.insert(0, GUI_DIR)

# ── Colour / Style Tokens ────────────────────────────────────────────────────
C_BG        = "#0f1117"   # window background
C_PANEL     = "#1a1d27"   # sidebar / panel
C_CARD      = "#1e2130"   # card surfaces
C_BORDER    = "#2a2d3e"   # subtle borders
C_ACCENT    = "#4f8ef7"   # primary blue
C_ACCENT2   = "#3ecf8e"   # success green
C_WARN      = "#f59e0b"   # amber warning
C_ERROR     = "#ef4444"   # red error
C_TEXT      = "#e2e8f0"   # primary text
C_MUTED     = "#64748b"   # secondary text
C_LOG_BG    = "#0a0c12"   # log console background
C_LOG_CMD   = "#a78bfa"   # collector output colour
C_LOG_OK    = "#34d399"   # success log colour
C_LOG_ERR   = "#f87171"   # error log colour
C_LOG_WARN  = "#fbbf24"   # warning log colour
C_LOG_INFO  = "#60a5fa"   # info log colour

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_SUB    = ("Segoe UI", 11, "bold")
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_LABEL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)
FONT_STATUS = ("Segoe UI", 9, "bold")

# ── Administrator Check ───────────────────────────────────────────────────────
def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
class CloudForixGUI:
    """Main application window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cloud Forix — Forensic Investigation Platform")
        self.root.geometry("1100x720")
        self.root.minsize(900, 600)
        self.root.configure(bg=C_BG)

        # Application state
        self._running   = False
        self._status    = "READY"
        self._inv_name  = tk.StringVar(value="Investigator")

        self._build_ui()
        self._check_admin_status()
        self._log("Cloud Forix GUI initialised. Ready to begin investigation.", "info")
        self._log(f"Python: {sys.executable}", "info")

    # ── UI Construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────────────────────────
        topbar = tk.Frame(self.root, bg=C_PANEL, height=56)
        topbar.pack(fill="x", side="top")
        topbar.pack_propagate(False)

        tk.Label(topbar, text="☁  CLOUD FORIX", font=FONT_TITLE,
                 bg=C_PANEL, fg=C_ACCENT).pack(side="left", padx=20, pady=10)
        tk.Label(topbar, text="Forensic Investigation Platform", font=FONT_LABEL,
                 bg=C_PANEL, fg=C_MUTED).pack(side="left", pady=10)

        # Admin badge
        self._admin_badge = tk.Label(topbar, text="", font=FONT_STATUS,
                                     bg=C_PANEL, fg=C_WARN)
        self._admin_badge.pack(side="right", padx=20)

        # Status pill
        self._status_var = tk.StringVar(value="● READY")
        self._status_lbl = tk.Label(topbar, textvariable=self._status_var,
                                    font=FONT_STATUS, bg=C_PANEL, fg=C_ACCENT2)
        self._status_lbl.pack(side="right", padx=16)

        # ── Main body (sidebar + content) ────────────────────────────────────
        body = tk.Frame(self.root, bg=C_BG)
        body.pack(fill="both", expand=True)

        sidebar = tk.Frame(body, bg=C_PANEL, width=220)
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)

        content = tk.Frame(body, bg=C_BG)
        content.pack(fill="both", expand=True, side="left")

        self._build_sidebar(sidebar)
        self._build_content(content)

    def _build_sidebar(self, parent):
        tk.Label(parent, text="INVESTIGATION", font=("Segoe UI", 8, "bold"),
                 bg=C_PANEL, fg=C_MUTED).pack(pady=(18, 4), padx=16, anchor="w")

        # Investigator name entry
        name_frame = tk.Frame(parent, bg=C_PANEL)
        name_frame.pack(fill="x", padx=12, pady=(0, 12))
        tk.Label(name_frame, text="Investigator:", font=FONT_LABEL,
                 bg=C_PANEL, fg=C_MUTED).pack(anchor="w")
        name_entry = tk.Entry(name_frame, textvariable=self._inv_name,
                              font=FONT_LABEL, bg=C_CARD, fg=C_TEXT,
                              insertbackground=C_TEXT, relief="flat",
                              highlightthickness=1, highlightbackground=C_BORDER,
                              highlightcolor=C_ACCENT)
        name_entry.pack(fill="x", ipady=5)

        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", padx=12, pady=6)
        tk.Label(parent, text="ACTIONS", font=("Segoe UI", 8, "bold"),
                 bg=C_PANEL, fg=C_MUTED).pack(pady=(4, 6), padx=16, anchor="w")

        buttons = [
            ("▶  Start Full Investigation", self._btn_full_investigation, C_ACCENT),
            ("📡  Collect Evidence",          self._btn_collect_evidence,     C_ACCENT),
            ("🔍  Run Threat Detection",      self._btn_threat_detection,     C_ACCENT),
            ("🔒  Verify Integrity",          self._btn_verify_integrity,     C_ACCENT),
            ("📄  Generate Report",           self._btn_generate_report,      C_ACCENT),
        ]
        self._action_buttons = []
        for label, cmd, _ in buttons:
            btn = tk.Button(parent, text=label, font=FONT_BTN, command=cmd,
                            bg=C_CARD, fg=C_TEXT, activebackground=C_ACCENT,
                            activeforeground="white", relief="flat", anchor="w",
                            padx=14, pady=8, cursor="hand2",
                            highlightthickness=0)
            btn.pack(fill="x", padx=10, pady=2)
            self._bind_hover(btn)
            self._action_buttons.append(btn)

        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", padx=12, pady=10)
        tk.Label(parent, text="VIEW", font=("Segoe UI", 8, "bold"),
                 bg=C_PANEL, fg=C_MUTED).pack(pady=(0, 6), padx=16, anchor="w")

        view_buttons = [
            ("📁  View Evidence Files",   self._btn_view_evidence),
            ("🚨  View Alerts",           self._btn_view_alerts),
            ("📊  View Reports",          self._btn_view_reports),
            ("🗄   View Database",         self._btn_view_database),
        ]
        for label, cmd in view_buttons:
            btn = tk.Button(parent, text=label, font=FONT_BTN, command=cmd,
                            bg=C_PANEL, fg=C_MUTED, activebackground=C_CARD,
                            activeforeground=C_TEXT, relief="flat", anchor="w",
                            padx=14, pady=7, cursor="hand2",
                            highlightthickness=0)
            btn.pack(fill="x", padx=10, pady=1)
            self._bind_hover(btn, hover_bg=C_CARD, hover_fg=C_TEXT)

        # Spacer + exit
        tk.Frame(parent, bg=C_PANEL).pack(fill="y", expand=True)
        tk.Frame(parent, bg=C_BORDER, height=1).pack(fill="x", padx=12, pady=6)
        exit_btn = tk.Button(parent, text="✕  Exit", font=FONT_BTN,
                             command=self._safe_exit,
                             bg=C_PANEL, fg=C_ERROR, activebackground=C_ERROR,
                             activeforeground="white", relief="flat", anchor="w",
                             padx=14, pady=8, cursor="hand2",
                             highlightthickness=0)
        exit_btn.pack(fill="x", padx=10, pady=(0, 12))

    def _build_content(self, parent):
        # ── Stats row ────────────────────────────────────────────────────────
        stats_row = tk.Frame(parent, bg=C_BG)
        stats_row.pack(fill="x", padx=16, pady=(14, 0))

        self._stat_evidence   = self._stat_card(stats_row, "Evidence Collected", "0")
        self._stat_hashes     = self._stat_card(stats_row, "Hashes Generated",   "0")
        self._stat_alerts     = self._stat_card(stats_row, "Alerts Detected",    "0")
        self._stat_integrity  = self._stat_card(stats_row, "Integrity Status",   "—")

        # ── Admin warning ────────────────────────────────────────────────────
        self._admin_warn_frame = tk.Frame(parent, bg=C_WARN)
        self._admin_warn_lbl   = tk.Label(
            self._admin_warn_frame,
            text="⚠  Not running as Administrator — Windows Security Event Log collection will be limited.",
            font=FONT_LABEL, bg=C_WARN, fg="#1a1a1a", padx=12, pady=6
        )
        self._admin_warn_lbl.pack(fill="x")

        # ── Log console ──────────────────────────────────────────────────────
        log_header = tk.Frame(parent, bg=C_BG)
        log_header.pack(fill="x", padx=16, pady=(10, 0))
        tk.Label(log_header, text="ACTIVITY LOG", font=("Segoe UI", 8, "bold"),
                 bg=C_BG, fg=C_MUTED).pack(side="left")
        tk.Button(log_header, text="Clear", font=("Segoe UI", 8),
                  command=self._clear_log, bg=C_CARD, fg=C_MUTED,
                  relief="flat", cursor="hand2", padx=8, pady=2).pack(side="right")

        log_frame = tk.Frame(parent, bg=C_LOG_BG,
                             highlightthickness=1, highlightbackground=C_BORDER)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        self._log_area = scrolledtext.ScrolledText(
            log_frame, bg=C_LOG_BG, fg=C_TEXT, font=FONT_MONO,
            relief="flat", wrap="word", state="disabled",
            insertbackground=C_TEXT
        )
        self._log_area.pack(fill="both", expand=True, padx=2, pady=2)

        # Tag colours
        self._log_area.tag_config("info",    foreground=C_LOG_INFO)
        self._log_area.tag_config("ok",      foreground=C_LOG_OK)
        self._log_area.tag_config("warn",    foreground=C_LOG_WARN)
        self._log_area.tag_config("error",   foreground=C_LOG_ERR)
        self._log_area.tag_config("cmd",     foreground=C_LOG_CMD)
        self._log_area.tag_config("ts",      foreground=C_MUTED)

    # ── Stat Cards ────────────────────────────────────────────────────────────
    def _stat_card(self, parent, label, value):
        frame = tk.Frame(parent, bg=C_CARD, padx=18, pady=12,
                         highlightthickness=1, highlightbackground=C_BORDER)
        frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        val_var = tk.StringVar(value=value)
        tk.Label(frame, textvariable=val_var, font=("Segoe UI", 22, "bold"),
                 bg=C_CARD, fg=C_ACCENT).pack(anchor="w")
        tk.Label(frame, text=label, font=FONT_LABEL, bg=C_CARD,
                 fg=C_MUTED).pack(anchor="w")
        return val_var

    # ── Hover helper ─────────────────────────────────────────────────────────
    def _bind_hover(self, btn, hover_bg=C_ACCENT, hover_fg="white"):
        orig_bg = btn.cget("bg")
        orig_fg = btn.cget("fg")
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg, fg=hover_fg))
        btn.bind("<Leave>", lambda e: btn.config(bg=orig_bg,  fg=orig_fg))

    # ── Admin Check ───────────────────────────────────────────────────────────
    def _check_admin_status(self):
        if is_admin():
            self._admin_badge.config(text="🔐 Administrator", fg=C_ACCENT2)
        else:
            self._admin_badge.config(text="⚠ Not Administrator", fg=C_WARN)
            self._admin_warn_frame.pack(fill="x", padx=16, pady=(6, 0))

    # ── Logging ───────────────────────────────────────────────────────────────
    def _log(self, msg: str, tag: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")

        def _write():
            self._log_area.config(state="normal")
            self._log_area.insert("end", f"[{ts}] ", "ts")
            self._log_area.insert("end", msg + "\n", tag)
            self._log_area.config(state="disabled")
            self._log_area.see("end")

        self.root.after(0, _write)

    def _clear_log(self):
        self._log_area.config(state="normal")
        self._log_area.delete("1.0", "end")
        self._log_area.config(state="disabled")

    # ── Status management ─────────────────────────────────────────────────────
    def _set_status(self, status: str):
        self._status = status
        colours = {
            "READY":     ("● READY",     C_ACCENT2),
            "RUNNING":   ("⟳ RUNNING",  C_WARN),
            "COMPLETED": ("✓ COMPLETED", C_ACCENT2),
            "ERROR":     ("✕ ERROR",     C_ERROR),
        }
        text, colour = colours.get(status, ("● READY", C_ACCENT2))
        self.root.after(0, lambda: self._status_var.set(text))
        self.root.after(0, lambda: self._status_lbl.config(fg=colour))

    def _lock_buttons(self):
        for btn in self._action_buttons:
            btn.config(state="disabled", fg=C_MUTED)

    def _unlock_buttons(self):
        for btn in self._action_buttons:
            btn.config(state="normal", fg=C_TEXT)

    # ── Thread runner ─────────────────────────────────────────────────────────
    def _run_in_thread(self, target, *args):
        """Run *target* in a daemon thread so the GUI never freezes."""
        if self._running:
            messagebox.showwarning("Busy",
                "An investigation is already running.\nPlease wait for it to finish.")
            return
        self._running = True
        self._lock_buttons()
        self._set_status("RUNNING")

        def _worker():
            try:
                target(*args)
                self._set_status("COMPLETED")
            except Exception as exc:
                self._set_status("ERROR")
                tb = traceback.format_exc()
                self._log(f"UNHANDLED ERROR: {exc}", "error")
                self._log(tb, "error")
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"An error occurred:\n{exc}"))
            finally:
                self._running = False
                self.root.after(0, self._unlock_buttons)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    # ─────────────────────────────────────────────────────────────────────────
    # BUTTON ACTIONS — call existing modules, never duplicate logic
    # ─────────────────────────────────────────────────────────────────────────

    def _btn_full_investigation(self):
        investigator = self._inv_name.get().strip()
        if not investigator:
            messagebox.showwarning("Missing Name", "Please enter an investigator name.")
            return
        self._run_in_thread(self._task_full_investigation, investigator)

    def _task_full_investigation(self, investigator: str):
        self._log(f"=== Full Investigation Started | Investigator: {investigator} ===", "cmd")

        # ── Step 1: DB ────────────────────────────────────────────────────────
        self._log("Initialising forensic database…", "info")
        from database import create_database
        create_database()
        self._log("Database ready.", "ok")

        # ── Step 2: Collectors ────────────────────────────────────────────────
        self._log("Starting evidence collection…", "info")
        log_files = self._collect_all_logs()

        # ── Step 3: Evidence processing ───────────────────────────────────────
        all_evidence, all_hashes, all_integrity = [], [], []
        all_ips, all_emails, all_activities, all_timestamps = [], [], [], []
        all_alerts = []

        from hash_module         import generate_hash
        from blockchain_api      import store_hash
        from encryption_module   import encrypt_file
        from integrity_verifier  import verify_integrity
        from metadata_extractor  import extract_metadata
        from database            import insert_evidence, insert_hash
        from access_logger       import log_access

        ev_count = 0
        for filepath in log_files:
            if filepath and os.path.exists(filepath):
                fname = os.path.basename(filepath)
                self._log(f"Processing: {fname}", "cmd")

                meta = extract_metadata(filepath)
                all_ips.extend(meta.get("ip_addresses", []))
                all_emails.extend(meta.get("emails", []))
                all_activities.extend(meta.get("activities", []))
                all_timestamps.extend(meta.get("timestamps", []))

                file_hash = generate_hash(filepath)
                self._log(f"SHA-256: {file_hash[:32]}…", "info")

                store_hash(fname, file_hash)
                insert_evidence(fname, filepath, "Cloud Log")
                insert_hash(fname, file_hash)

                try:
                    os.makedirs("evidence", exist_ok=True)
                    encrypt_file(filepath)
                    self._log(f"Encrypted: evidence/{fname}.enc", "ok")
                except Exception as enc_err:
                    self._log(f"Encryption skipped ({fname}): {enc_err}", "warn")

                integrity = verify_integrity(fname, file_hash)
                self._log(f"Integrity [{fname}]: {integrity}", "ok" if integrity == "Verified" else "warn")

                if integrity != "Verified":
                    all_alerts.append(f"Integrity check failed: {fname}")

                log_access(fname, investigator)

                all_evidence.append(fname)
                all_hashes.append(file_hash)
                all_integrity.append(integrity)
                ev_count += 1

        self.root.after(0, lambda n=ev_count: self._stat_evidence.set(str(n)))
        self.root.after(0, lambda n=ev_count: self._stat_hashes.set(str(n)))

        # ── Step 4: Threat detection ──────────────────────────────────────────
        self._log("Running threat detection…", "info")
        detection_alerts = self._run_detectors()
        all_alerts.extend(detection_alerts)

        alert_count = len(all_alerts)
        self.root.after(0, lambda n=alert_count: self._stat_alerts.set(str(n)))

        if all_alerts:
            self._log(f"{alert_count} alert(s) detected.", "warn")
            self._log("Sending email alert…", "info")
            from email_alert import send_email_alert
            send_email_alert("\n".join(all_alerts))
        else:
            self._log("No alerts detected.", "ok")

        # ── Step 5: Report ────────────────────────────────────────────────────
        self._log("Generating final report…", "info")
        from report_generator import generate_report
        generate_report(investigator, all_evidence, all_hashes, all_integrity,
                        all_ips, all_alerts, all_emails, all_activities, all_timestamps)

        # integrity summary
        verified = sum(1 for i in all_integrity if i == "Verified")
        total    = len(all_integrity)
        summary  = f"{verified}/{total} Verified" if total else "No evidence"
        self.root.after(0, lambda s=summary: self._stat_integrity.set(s))

        self._log("=== Investigation Completed Successfully ===", "ok")

    # ── Collect evidence ──────────────────────────────────────────────────────
    def _btn_collect_evidence(self):
        self._run_in_thread(self._task_collect_evidence)

    def _task_collect_evidence(self):
        self._log("=== Evidence Collection Started ===", "cmd")
        from database import create_database
        create_database()
        log_files = self._collect_all_logs()
        ev_count = sum(1 for f in log_files if f and os.path.exists(f))
        self.root.after(0, lambda n=ev_count: self._stat_evidence.set(str(n)))
        self._log(f"=== Collection Complete — {ev_count} log file(s) collected ===", "ok")

    def _collect_all_logs(self) -> list:
        """Call all existing collectors and return list of output file paths."""
        results = []

        collectors = [
            ("DNS logs",          "DNS_log_collector",        "collect_dns_logs"),
            ("Network logs",      "network_log_collector",    "collect_network_logs"),
            ("System logs",       "system_log_collector",     "collect_system_logs"),
            ("Google Drive logs", "google_cloud_logs",        "collect_google_drive_logs"),
            ("OneDrive logs",     "onedrive_logs",            "collect_onedrive_logs"),
            ("Azure AD logs",     "azure_ad_logs_collector",  "collect_azure_logs"),
            ("MDE logs",          "mde_collector",            "collect_mde_logs"),
            ("EMS logs",          "ems_web_collector",        "collect_ems_logs"),
        ]

        for display_name, module_name, func_name in collectors:
            self._log(f"Collecting {display_name}…", "info")
            try:
                import importlib
                mod  = importlib.import_module(module_name)
                func = getattr(mod, func_name)
                result = func()
                results.append(result)
                self._log(f"{display_name}: collected → {result}", "ok")
            except Exception as exc:
                self._log(f"{display_name}: {exc}", "warn")
                results.append(None)

        return results

    # ── Threat detection ──────────────────────────────────────────────────────
    def _btn_threat_detection(self):
        self._run_in_thread(self._task_threat_detection)

    def _task_threat_detection(self):
        self._log("=== Threat Detection Started ===", "cmd")
        alerts = self._run_detectors()
        alert_count = len(alerts)
        self.root.after(0, lambda n=alert_count: self._stat_alerts.set(str(n)))
        if alerts:
            self._log(f"{alert_count} alert(s) found:", "warn")
            for a in alerts:
                self._log(f"  → {a}", "warn")
        else:
            self._log("No threats detected.", "ok")
        self._log("=== Threat Detection Complete ===", "ok")

    def _run_detectors(self) -> list:
        """Run all existing detection modules and return combined alerts."""
        alerts = []

        # Malware
        self._log("Running malware detector (VirusTotal)…", "info")
        try:
            from malware_detector import detect_malware
            malware_alerts = detect_malware()
            alerts.extend(malware_alerts)
            self._log(f"Malware scan complete — {len(malware_alerts)} alert(s).", "ok")
        except Exception as e:
            self._log(f"Malware detector error: {e}", "warn")

        # Unauthorised access (win32evtlog)
        self._log("Running unauthorised access detector (Windows Event Log)…", "info")
        if not is_admin():
            self._log("⚠ Not running as Administrator — Security log may be inaccessible.", "warn")
        try:
            from unauthorized_access_detector import detect_unauthorized_access
            unauth_alerts = detect_unauthorized_access()
            alerts.extend(unauth_alerts)
            self._log(f"Unauthorised access scan complete — {len(unauth_alerts)} alert(s).", "ok")
        except Exception as e:
            self._log(f"Unauthorised access detector error: {e}", "warn")

        # Network
        self._log("Running network attack detector…", "info")
        try:
            from network_attack_detector import detect_suspicious_connections
            net_alerts = detect_suspicious_connections()
            alerts.extend(net_alerts)
            self._log(f"Network scan complete — {len(net_alerts)} alert(s).", "ok")
        except Exception as e:
            self._log(f"Network attack detector error: {e}", "warn")

        return alerts

    # ── Verify integrity ──────────────────────────────────────────────────────
    def _btn_verify_integrity(self):
        self._run_in_thread(self._task_verify_integrity)

    def _task_verify_integrity(self):
        self._log("=== Integrity Verification Started ===", "cmd")

        blockchain_file = os.path.join(GUI_DIR, "blockchain", "blockchain.json")
        if not os.path.exists(blockchain_file):
            self._log("No blockchain file found. Collect evidence first.", "warn")
            return

        import json
        from hash_module        import generate_hash
        from integrity_verifier import verify_integrity

        with open(blockchain_file, "r") as f:
            chain = json.load(f)

        if not chain:
            self._log("Blockchain is empty. No records to verify.", "warn")
            return

        verified = 0
        failed   = 0
        for block in chain:
            eid       = block.get("evidence_id", "")
            stored_h  = block.get("evidence_hash", "")
            # Try to find the log file
            candidate = os.path.join(GUI_DIR, "logs", eid)
            if os.path.exists(candidate):
                live_hash = generate_hash(candidate)
                status    = verify_integrity(eid, live_hash)
                tag       = "ok" if status == "Verified" else "error"
                self._log(f"[{eid}] → {status}", tag)
                if status == "Verified":
                    verified += 1
                else:
                    failed += 1
            else:
                self._log(f"[{eid}] → file not found (encrypted evidence)", "warn")

        summary = f"{verified} Verified / {failed} Failed"
        self.root.after(0, lambda s=summary: self._stat_integrity.set(s))
        self._log(f"=== Integrity Check Complete: {summary} ===", "ok")

    # ── Generate report ───────────────────────────────────────────────────────
    def _btn_generate_report(self):
        investigator = self._inv_name.get().strip() or "Unknown"
        self._run_in_thread(self._task_generate_report, investigator)

    def _task_generate_report(self, investigator: str):
        self._log("=== Generating Report ===", "cmd")
        try:
            from report_generator import generate_report
            generate_report(investigator, [], [], [], [], [], [], [], [])
            import glob
            reports = sorted(glob.glob(os.path.join(GUI_DIR, "reports", "Final_Report_*.txt")))
            if reports:
                self._log(f"Report saved: {os.path.basename(reports[-1])}", "ok")
            self._log("=== Report Generation Complete ===", "ok")
        except Exception as e:
            self._log(f"Report error: {e}", "error")
            raise

    # ── View panels ───────────────────────────────────────────────────────────
    def _btn_view_evidence(self):
        self._show_file_list("Evidence Files", os.path.join(GUI_DIR, "evidence"),
                             "*.enc", "No encrypted evidence files found.\nRun an investigation first.")

    def _btn_view_alerts(self):
        """Show alerts from the database."""
        self._log("Loading alerts from database…", "info")
        try:
            import sqlite3
            db_path = os.path.join(GUI_DIR, "forensic.db")
            if not os.path.exists(db_path):
                messagebox.showinfo("No Database", "Database not found. Run an investigation first.")
                return
            conn   = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT alert, timestamp FROM alerts ORDER BY timestamp DESC LIMIT 200")
            rows = cursor.fetchall()
            conn.close()

            win   = tk.Toplevel(self.root)
            win.title("Alerts")
            win.geometry("700x450")
            win.configure(bg=C_BG)
            tk.Label(win, text=f"Alerts ({len(rows)} records)",
                     font=FONT_SUB, bg=C_BG, fg=C_TEXT).pack(pady=10)

            txt = scrolledtext.ScrolledText(win, bg=C_LOG_BG, fg=C_TEXT,
                                            font=FONT_MONO, relief="flat")
            txt.pack(fill="both", expand=True, padx=12, pady=(0, 12))
            if rows:
                for alert, ts in rows:
                    txt.insert("end", f"[{ts}] {alert}\n")
            else:
                txt.insert("end", "No alerts recorded.")
            txt.config(state="disabled")
        except Exception as e:
            self._log(f"Alert view error: {e}", "error")
            messagebox.showerror("Error", str(e))

    def _btn_view_reports(self):
        self._show_file_list("Investigation Reports", os.path.join(GUI_DIR, "reports"),
                             "Final_Report_*.txt", "No reports found. Generate a report first.",
                             openable=True)

    def _btn_view_database(self):
        """Show evidence and hash counts from the DB."""
        try:
            import sqlite3
            db_path = os.path.join(GUI_DIR, "forensic.db")
            if not os.path.exists(db_path):
                messagebox.showinfo("No Database", "Database not found. Run an investigation first.")
                return
            conn = sqlite3.connect(db_path)
            c    = conn.cursor()
            c.execute("SELECT COUNT(*) FROM evidence"); ev_count  = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM hashes");   hash_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM alerts");   al_count  = c.fetchone()[0]
            c.execute("SELECT evidence_id, file_path, source, collected_time FROM evidence ORDER BY collected_time DESC LIMIT 100")
            rows = c.fetchall()
            conn.close()

            win = tk.Toplevel(self.root)
            win.title("Forensic Database")
            win.geometry("800x500")
            win.configure(bg=C_BG)
            tk.Label(win, text="Forensic Database", font=FONT_SUB,
                     bg=C_BG, fg=C_TEXT).pack(pady=10)
            summary = f"Evidence: {ev_count}  |  Hashes: {hash_count}  |  Alerts: {al_count}"
            tk.Label(win, text=summary, font=FONT_LABEL, bg=C_BG,
                     fg=C_MUTED).pack()

            cols = ("Evidence ID", "File Path", "Source", "Collected At")
            tree = ttk.Treeview(win, columns=cols, show="headings", height=18)
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview", background=C_CARD, foreground=C_TEXT,
                            fieldbackground=C_CARD, rowheight=24,
                            font=FONT_LABEL)
            style.configure("Treeview.Heading", background=C_PANEL,
                            foreground=C_MUTED, font=("Segoe UI", 8, "bold"))
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=180, anchor="w")
            for row in rows:
                tree.insert("", "end", values=row)

            sb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=sb.set)
            tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(8, 12))
            sb.pack(side="right", fill="y", padx=(0, 12), pady=(8, 12))
        except Exception as e:
            self._log(f"Database view error: {e}", "error")
            messagebox.showerror("Error", str(e))

    def _show_file_list(self, title, directory, pattern, empty_msg, openable=False):
        import glob
        files = sorted(glob.glob(os.path.join(directory, pattern)))

        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("650x380")
        win.configure(bg=C_BG)
        tk.Label(win, text=f"{title} ({len(files)} files)",
                 font=FONT_SUB, bg=C_BG, fg=C_TEXT).pack(pady=10)

        lb_frame = tk.Frame(win, bg=C_BG)
        lb_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        lb = tk.Listbox(lb_frame, bg=C_CARD, fg=C_TEXT, font=FONT_MONO,
                        relief="flat", selectbackground=C_ACCENT,
                        highlightthickness=0, activestyle="none")
        sb = ttk.Scrollbar(lb_frame, orient="vertical", command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        lb.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        if files:
            for f in files:
                size = os.path.getsize(f)
                lb.insert("end", f"{os.path.basename(f)}  ({size:,} bytes)")
        else:
            lb.insert("end", empty_msg)

        if openable and files:
            def _open_selected():
                sel = lb.curselection()
                if sel:
                    path = files[sel[0]]
                    try:
                        os.startfile(path)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

            tk.Button(win, text="Open Selected", font=FONT_BTN, command=_open_selected,
                      bg=C_ACCENT, fg="white", relief="flat", padx=12, pady=6).pack(pady=6)

    # ── Exit ─────────────────────────────────────────────────────────────────
    def _safe_exit(self):
        if self._running:
            if not messagebox.askyesno("Confirm Exit",
                "An investigation is running. Exit anyway?"):
                return
        self.root.destroy()


# ─────────────────────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()

    # DPI awareness on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    root.tk.call("tk", "scaling", 1.3)

    app = CloudForixGUI(root)
    root.protocol("WM_DELETE_WINDOW", app._safe_exit)
    root.mainloop()


if __name__ == "__main__":
    main()
