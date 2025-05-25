import sqlite3
from config import DB_PATH

# Replace with actual username you want to make admin
username_to_promote = "gotohell"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (username_to_promote,))
conn.commit()
conn.close()

print(f"✅ Admin status updated for '{username_to_promote}'")   
