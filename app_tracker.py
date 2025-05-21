import sqlite3
from datetime import datetime

DB_PATH = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            url TEXT UNIQUE,
            applied_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_application(company, role, url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO applications (company, role, url, applied_at)
            VALUES (?, ?, ?, ?)
        ''', (company, role, url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        print(f"[+] Logged: {company} – {role}")
    except sqlite3.IntegrityError:
        print(f"[!] Already applied to: {url}")
    finally:
        conn.close()

def has_applied(url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM applications WHERE url = ?', (url,))
    result = cursor.fetchone()[0] > 0
    conn.close()
    return result

# ✅ Run this once to initialize the DB
if __name__ == "__main__":
    init_db()
