import streamlit as st
from datetime import datetime
import numpy as np
from storage import save_prediction


def show_stress_monitor(username, model=None):
    st.title("🧠 Stress Monitor")

    st.markdown("### Please answer the following questions:")
    sleep_hours = st.slider("How many hours do you sleep daily?", 0, 18, 6)
    work_hours = st.slider("How many hours do you work daily?", 0, 20, 8)
    exercise = st.radio("Do you exercise regularly?", ["Yes", "No"])
    appetite = st.radio("How is your appetite?", ["Normal", "Low", "High"])
    mood = st.slider("On a scale of 1-10, how would you rate your current mood?", 1, 10, 5)

    if st.button("Check Stress Level"):
        st.write("USERNAME:", username) 
        score = 0
        if sleep_hours < 6:
            score += 2
        if work_hours > 8:
            score += 2
        if exercise == "No":
            score += 1
        if appetite != "Normal":
            score += 1
        if mood <= 4:
            score += 2

        if score >= 5:
            stress_level = "High"
        elif score >= 3:
            stress_level = "Moderate"
        else:
            stress_level = "Low"

        st.success(f"Your estimated stress level is: **{stress_level}**")

        if username:
            input_data = {
                "sleep_hours": sleep_hours,
                "work_hours": work_hours,
                "exercise": exercise,
                "appetite": appetite,
                "mood": mood
            }
            prediction_result = {
                "stress_level": stress_level
            }

            save_prediction(
                username=username,
                service="Stress Monitor",
                input_data=input_data,
                prediction_result=prediction_result,
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            st.info("Prediction saved successfully ✅")
