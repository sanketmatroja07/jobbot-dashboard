import sqlite3

DB_PATH = "tracker.db"

def patch_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get existing column names
    cursor.execute("PRAGMA table_info(applications)")
    columns = [col[1] for col in cursor.fetchall()]

    # Add missing columns
    if 'status' not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN status TEXT DEFAULT 'submitted'")
        print("[+] Added 'status' column")

    if 'feedback' not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN feedback TEXT")
        print("[+] Added 'feedback' column")

    conn.commit()
    conn.close()
    print("✅ Database patch complete.")

if __name__ == "__main__":
    patch_database()
