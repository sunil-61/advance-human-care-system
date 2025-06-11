# services/diabetes.py

import streamlit as st
import numpy as np
from datetime import datetime
from storage import save_prediction

def show_diabetes_prediction(model = None, username = None):
    st.title("🩺 Enter Details for Diabetes Prediction")
    st.write("If will give you a prediction of your diabetes based on your daily routine, genetic details and personal life!")

    st.subheader("Enter Your Details")

    agee = st.slider("What is Your Age?", 1, 100, 6)
    gender = st.radio("What is Your Gender?", ["Male", "Female"])
    weight = st.number_input("Enter Your Weight (in kg)",min_value=10.0, max_value=200.0, value=60.0)
    height = st.number_input("Enter Your Height (in cm)",min_value=50.0, max_value=250.0, value=170.0)
    bodymassindex = weight / ((height/100)**2)
    family = st.radio("Family History of Diabetes?", ["No", "1 Parent", "Both Parent"])
    physical = st.slider("How Many Minutes Did You Do Physical Activity Today?",0,180,30)
    systolic = st.slider("Your upper bp count?",80,200,120)
    diastolic = st.slider("Your Lower bp count?",40,130,80)
    score = 0
    st.subheader("AI Suggestions")
    suggestions = []
    if systolic < 90 or diastolic < 60:
        score += 1
        st.warning("Low Blood Pressure")
        suggestions.append("Thoda Namak paani pi lena!")
    elif 90 <= systolic <= 120 and 60 <= diastolic <= 80:
        score += 0
        st.success("Normal Blood Pressure")
    elif 121 <= systolic <= 139 or 81 <= diastolic <= 89:
        score += 1
        st.info("Pre-hypertension")
        suggestions.append("Blood Pressure bad rha hai dhyan de!")
    elif systolic >= 140 or diastolic >= 90:
        score += 2
        st.error("High Blood Pressure")
        suggestions.append("Doctor se milne ka time aa gya hai bhai!")
    
    frequent_urination = st.radio("Frequent Urination?",["Yes", "No"])

    if st.button("🔍 Diabetes Prediction"):
        #Age Calculate
        if agee < 35:
            score += 0
        elif agee < 50:
            score += 1
        else:
            score += 2

        #using Gender
        if gender == "Male":
            score += 1
        elif gender == "Female":
            score += 1
        else:
            st.warning("Wrong Input!")

        #Body Mass Index
        if bodymassindex < 25:
            score += 0
        elif bodymassindex <= 30:
            score += 1
        else:
            score += 2

        #Family History
        if family == "No":
            score += 0
        elif family == "Parent":
            score += 1
        elif family == "Both Parent":
            score += 2
        else:
            st.warning("Wrong Input!")

        #Physical Activity
        if physical == 0:
            score += 2
        elif physical < 40:
            score += 1
        else:
            score += 0

        #Frequent Urination
        if frequent_urination == "Yes":
            score += 2
        elif frequent_urination == "No":
            score += 0
        else:
            st.warning("Wrong Input!")

        #Prediction of Diabetes
        if score <= 4:
            st.error("Low Risk")
        elif score <= 7:
            st.success("Normal Risk")
        else:
            st.warning("High Risk")
        
        if username:
            input_data = {
                "age": agee,
                "gender": gender,
                "weight": weight,
                "height": height,
                "BMI": round(bodymassindex, 2),
                "family": family,
                "physical": physical,
                "systolic": systolic,
                "diastolic": diastolic,
                "frequent_urination": frequent_urination 
                }
            prediction_result = {
                "score": score,
                "result": "Low Risk" if score <= 4 else "Normal Risk" if score <= 7 else "High Risk",
                "suggestions": suggestions 
                }

            save_prediction(
                username=username,
                service="Diabetes Prediction",
                input_data=input_data,
                prediction_result=prediction_result,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ) 
            st.info("Prediction saved successfully ✅")