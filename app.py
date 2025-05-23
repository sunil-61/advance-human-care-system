import streamlit as st
import numpy as np
import pickle
import login  # Make sure login.py is in the same directory

# Session initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# If not logged in, show login/signup page
if not st.session_state.logged_in:
    login.show_login_page()

# If logged in, show prediction interface
else:
    # 🟨 Sidebar: Help + Logout
    with st.sidebar:
        st.header("❓ Help")
        if st.button("View Help"):
            st.info("""
            - This app predicts diabetes based on medical input data.
            - Enter values for each field and click **Predict**.
            - Model used: Random Forest Classifier.
            - Dataset: PIMA Indian Diabetes Dataset.
            """)

        # 🚪 Logout Button
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.experimental_rerun()

    # 🧠 Diabetes Prediction App
    st.title("🧠 Diabetes Prediction App")

    # Load trained model
    model = pickle.load(open('diabetes_model.pkl', 'rb'))

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

