import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect("forensic.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evidence (
        evidence_id TEXT,
        file_path TEXT,
        source TEXT,
        collected_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hashes (
        evidence_id TEXT,
        hash_value TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        alert TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_evidence(evidence_id, file_path, source):
    conn = sqlite3.connect("forensic.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO evidence VALUES (?, ?, ?, ?)",
                   (evidence_id, file_path, source, str(datetime.now())))

    conn.commit()
    conn.close()


def insert_hash(evidence_id, hash_value):
    conn = sqlite3.connect("forensic.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO hashes VALUES (?, ?, ?)",
                   (evidence_id, hash_value, str(datetime.now())))

    conn.commit()
    conn.close()


def insert_alert(alert):
    conn = sqlite3.connect("forensic.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO alerts VALUES (?, datetime('now'))", (alert,))

    conn.commit()
    conn.close()