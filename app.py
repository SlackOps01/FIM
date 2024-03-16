import os 
import hashlib
import sqlite3
import time
from datetime import datetime
from plyer import notification

directory_to_monitor = "C:\\Users\\Administrator\\Desktop\\VICTIM"
conn = sqlite3.connect("data.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    file_path TEXT NOT NULL UNIQUE,
    hash_value TEXT NOT NULL,
    last_modified TIMESTAMP NOT NULL
)
"""
)
conn.commit()

def calculate_hash(file_path):
    with open(file_path, "rb") as file_obj:
        hash_value = hashlib.file_digest(file_obj, "sha256").hexdigest()
        
    return hash_value

def update_file_hashes() -> None:
    for root, dirs, files in os.walk(directory_to_monitor):
        for file in files:
            file_path = os.path.join(root, file)
            hash_value = calculate_hash(file_path)
            last_modified = os.path.getmtime(file_path)
            c.execute("""
                INSERT OR REPLACE INTO files (file_path, hash_value, last_modified)
                VALUES (?, ?, ?)
            """, (file_path, hash_value, last_modified))
            
    conn.commit()

def check_integrity():
    c.execute("SELECT file_path, hash_value, last_modified FROM files")
    rows = c.fetchall()
    for row in rows:
        file_path, stored_hash, last_modified = row
        current_hash = calculate_hash(file_path)
        if current_hash != stored_hash:
            print(f"Integrity violation detected for file: {file_path}")
            notify_user(file_path, last_modified)

def notify_user(file_path, last_modified):
    last_modified_str = datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
    notification_title = "File Integrity Violation Detected"
    notification_message = f"File integrity violation detected for file: {file_path}\nLast modified: {last_modified_str}"
    notification.notify(
        title=notification_title,
        message=notification_message,
        app_name="File Integrity Monitor",
        timeout=10
    )
if __name__ == "__main__":
    update_file_hashes()

    while True:
        check_integrity()
        time.sleep(60)

conn.close()