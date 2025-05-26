import streamlit as st
import numpy as np
from datetime import datetime
from storage import save_prediction

def show_habit_monitor(model=None, username=None):
    st.title("🧠 AI Habit Tracker")
    st.write("Track your daily habits and get smart suggestions to improve your lifestyle.")

    st.subheader("Enter Your Daily Habits")

    water_intake = st.slider("How many glasses of water did you drink today?", 0, 15, 5)
    screen_time = st.slider("How many hours did you use mobile/laptop?", 0, 15, 6)
    sleep_hours = st.slider("How many hours did you sleep?", 0, 12, 7)
    study_hours = st.slider("How many hours did you study/work productively?", 0, 12, 3)

    # ---- AI SUGGESTIONS ----
    st.subheader("AI Suggestions")

    def generate_suggestion(water, screen, sleep, study):
        suggestions = []

        if water < 6:
            suggestions.append("Paani kam piya bhai, kam se kam 6 glass toh banta hai!")
        else:
            suggestions.append("Good! Hydration on point.")

        if screen > 6:
            suggestions.append("Screen time zyada ho gaya. Aankhon ko rest de, blue light khatarnaak hai.")
        else:
            suggestions.append("Nice! Screen time thik-thak hai.")

        if sleep < 7:
            suggestions.append("Neend puri nahi hui. 7-8 ghante ki neend zaroori hai.")
        else:
            suggestions.append("Sleep check! Tagda rest le raha hai.")

        if study < 2:
            suggestions.append("Kaam thoda kam kiya aaj. Kal thoda extra push maar bhai.")
        else:
            suggestions.append("Nice productivity! Keep it up.")

        return suggestions

    suggestions = generate_suggestion(water_intake, screen_time, sleep_hours, study_hours)

    for i, suggestion in enumerate(suggestions):
        st.write(f"**{i+1}.** {suggestion}")

    # ---- SCORE SYSTEM ----
    score = np.mean([
        min(water_intake / 8, 1),
        1 - min(screen_time / 10, 1),
        min(sleep_hours / 8, 1),
        min(study_hours / 4, 1)
    ]) * 100

    st.subheader("Your Daily Score")
    st.progress(int(score))
    st.success(f"Today's Habit Score: **{int(score)} / 100**")

    # ---- SAVE TO STORAGE ----
    if username is None:
        st.error("User not logged in. Cannot save habit data.")
        return

    try:
        save_prediction(
            username=username,
            service="Habit Tracker",
            input_data={
                "water_intake": water_intake,
                "screen_time": screen_time,
                "sleep_hours": sleep_hours,
                "study_hours": study_hours
            },
            prediction_result={
                "score": int(score),
                "suggestions": suggestions
            },
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception as e:
        st.error(f"Failed to save data: {e}")

    st.markdown("---")
    st.caption(f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

