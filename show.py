import sqlite3
from config import DB_PATH

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Fetch all users and their admin status
c.execute("SELECT username, is_admin FROM users")
rows = c.fetchall()

# Print admin users
print("All users and admin status:\n")
for username, is_admin in rows:
    status = "✅ Admin" if is_admin == 1 else "User"
    print(f"Username: {username} --> {status}")

conn.close()
