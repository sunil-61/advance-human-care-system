import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import sqlite3

# 👇 Create complaints table in users.db if it doesn't exist
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        complaint TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

# 👇 Train and save model
data = pd.read_csv('diabetes.csv')
X = data.drop('Outcome', axis=1)
y = data['Outcome']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

with open('diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as diabetes_model.pkl")
print("✅ complaints table created (if not already present)")

