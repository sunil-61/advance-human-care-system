import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# 1. Load data
data = pd.read_csv('diabetes.csv')

# 2. Split features and target
X = data.drop('Outcome', axis=1)
y = data['Outcome']

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 5. Save model to file
with open('diabetes_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as diabetes_model.pkl")
