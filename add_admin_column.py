import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Check if column already exists
try:
    c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
    print("✅ 'is_admin' column added to 'users' table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ 'is_admin' column already exists.")
    else:
        print("❌ Error:", e)

conn.commit()
conn.close()
