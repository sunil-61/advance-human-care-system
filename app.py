import streamlit as st
import numpy as np
import pickle

# Load trained model
model = pickle.load(open('diabetes_model.pkl', 'rb'))

st.title("🧠 Diabetes Prediction App")


# Input fields
pregnancies = st.number_input("Pregnancies", 0, 20)
glucose = st.number_input("Glucose Level", 0, 300)
blood_pressure = st.number_input("Blood Pressure", 0, 200)
skin_thickness = st.number_input("Skin Thickness", 0, 100)
insulin = st.number_input("Insulin", 0, 900)
bmi = st.number_input("BMI", 0.0, 70.0)
dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
age = st.number_input("Age", 1, 120)

if st.button("🔍 Predict"):
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                            insulin, bmi, dpf, age]])
    
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("❌ The person is likely to have Diabetes.")
    else:
        st.success("✅ The person is unlikely to have Diabetes.")

with st.sidebar:
    st.header("❓ Help")
    if st.button("View Help"):
        st.info("""
        - This app predicts diabetes based on medical input data.
        - Enter values for each field and click **Predict**.
        - Model used: Random Forest Classifier.
        - Dataset: PIMA Indian Diabetes Dataset.
        """)

