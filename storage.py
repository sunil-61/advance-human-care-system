# storage.py

import sqlite3
from config import DB_PATH

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

def save_prediction(username, input_data, result):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO predictions (username, input_data, result) VALUES (?, ?, ?)', 
              (username, str(input_data), result))
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

