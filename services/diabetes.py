# services/diabetes.py

import streamlit as st
import numpy as np
from datetime import datetime
from storage import save_prediction

def show_diabetes_prediction(model, username):
    st.subheader("🩺 Enter Details for Diabetes Prediction")

    pregnancies = st.number_input("Pregnancies", 0, 20)
    glucose = st.number_input("Glucose Level", 0, 300)
    blood_pressure = st.number_input("Blood Pressure", 0, 200)
    skin_thickness = st.number_input("Skin Thickness", 0, 100)
    insulin = st.number_input("Insulin", 0, 900)
    bmi = st.number_input("BMI", 0.0, 70.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
    age = st.number_input("Age", 1, 120)

    if st.button("🔍 Predict"):
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
        prediction = model.predict(input_data)[0]
        result = "Positive" if prediction == 1 else "Negative"
        save_prediction(username, "Diabetes Prediction", input_data.tolist(), result, datetime.now())

        if prediction == 1:
            st.error("❌ High Risk of Diabetes")
        else:
            st.success("✅ Low Risk of Diabetes")

