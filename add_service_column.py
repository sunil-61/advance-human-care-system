import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("ALTER TABLE predictions ADD COLUMN service TEXT")
conn.commit()
conn.close()
print("Service column added successfully.")
