import sqlite3
import json
from config import DB_PATH

DB_PATH = 'users.db'


def create_prediction_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            username TEXT,
            input_data TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(username, service, input_data, prediction_result, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Make sure table exists (optional, safe initialization)
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            service TEXT,
            input_data TEXT,
            result TEXT,
            timestamp TEXT
        )
    ''')

    c.execute(
        'INSERT INTO predictions (username, service, input_data, result, timestamp) VALUES (?, ?, ?, ?, ?)',
        (
            username,
            service,
            json.dumps(input_data),
            json.dumps(prediction_result),
            timestamp
        )
    )

    conn.commit()
    conn.close()


def get_user_predictions(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT input_data, result, timestamp FROM predictions WHERE username = ? ORDER BY timestamp DESC', 
              (username,))
    results = c.fetchall()
    conn.close()
    return results

def delete_prediction(username, timestamp):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM predictions WHERE username = ? AND timestamp = ?', (username, timestamp))
    conn.commit()
    conn.close()

