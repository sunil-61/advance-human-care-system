import streamlit as st
import numpy as np
import pickle
import login
import sqlite3
import os
from config import DB_PATH
from storage import create_prediction_table, save_prediction, get_user_predictions, delete_prediction
import services.diabetes as diabetes
import services.stress as stress
import services.habit as habit

# Create required tables
create_prediction_table()
login.create_user_table()

# Load diabetes model
MODEL_PATH = "diabetes_model.pkl"
model = pickle.load(open(MODEL_PATH, "rb"))

# Streamlit settings
st.set_page_config(layout="wide")

# ---------------- Session State Initialization ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False
if "selected_service" not in st.session_state:
    st.session_state.selected_service = None

# ------------------- Helper Functions -------------------------

def get_user_data(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, mobile, email FROM users WHERE username = ?", (username,))
    data = c.fetchone()
    conn.close()
    return data

def update_user_profile(old_username, new_username, mobile, email):
    if login.user_exists(new_username) and old_username != new_username:
        return False, "Username already taken."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET username = ?, mobile = ?, email = ? WHERE username = ?",
              (new_username, mobile, email, old_username))
    conn.commit()
    conn.close()
    # Rename profile photo if username changed
    profile_dir = "profile_photos"
    old_photo_path = os.path.join(profile_dir, f"{old_username}.png")
    new_photo_path = os.path.join(profile_dir, f"{new_username}.png")
    if old_username != new_username and os.path.exists(old_photo_path):
        os.rename(old_photo_path, new_photo_path)
    st.session_state.username = new_username
    return True, "Profile updated successfully!"

def change_password(username, old_pass, new_pass):
    if not login.validate_user(username, old_pass):
        return False, "Old password incorrect."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed_new = login.hash_password(new_pass)
    c.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new, username))
    conn.commit()
    conn.close()
    return True, "Password changed successfully!"

# --------------------- Main UI -------------------------------

if not st.session_state.logged_in:
    login.show_login_signup_page()

else:
    # Top Menu
    col1, col2, col3 = st.columns([1, 1, 9])
    with col1:
        if st.button("🏠", help="Open Menu"):
            st.session_state.show_menu = not st.session_state.show_menu
            st.session_state.selected_service = None
    with col2:
        if st.button("🏃🚪", help="Log Out"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    with col3:
        service_selected = st.selectbox("📌 Services", ["Select Service", "Diabetes Prediction", "Stress Monitor", "AI Habit Tracker"])
        if service_selected != "Select Service":
            st.session_state.selected_service = service_selected
            st.session_state.show_menu = False
        else:
            st.session_state.selected_service = None

    # Load selected service
    services = {
        "Diabetes Prediction": diabetes.show_diabetes_prediction,
        "Stress Monitor": stress.show_stress_monitor,
        "AI Habit Tracker": habit.show_habit_monitor
    }

    if st.session_state.selected_service in services:
        if st.session_state.selected_service == "Diabetes Prediction":
            services["Diabetes Prediction"](model, st.session_state.username)
        else:
            services[st.session_state.selected_service](st.session_state.username)

    # Show home menu
    if st.session_state.show_menu and st.session_state.selected_service is None:
        st.markdown("---")
        menu_option = st.radio("Select an Option:", ["View Profile", "Change Password", "Prediction History", "Help", "Contact Us"], index=0)

        if menu_option == "View Profile":
            st.subheader("👤 View / Update Profile")
            user_data = get_user_data(st.session_state.username)
            new_username = st.text_input("Username", value=user_data[0])
            mobile = st.text_input("Mobile Number", value=user_data[1])
            email = st.text_input("Email ID", value=user_data[2])

            # Profile photo upload
            profile_dir = "profile_photos"
            os.makedirs(profile_dir, exist_ok=True)
            photo_path = os.path.join(profile_dir, f"{st.session_state.username}.png")

            uploaded_photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
            if uploaded_photo is not None:
                with open(photo_path, "wb") as f:
                    f.write(uploaded_photo.read())
                st.success("Profile photo updated successfully!")

            if os.path.exists(photo_path):
                st.image(photo_path, width=150, caption="Profile Photo")

            if st.button("Update Profile"):
                success, message = update_user_profile(st.session_state.username, new_username, mobile, email)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        elif menu_option == "Change Password":
            st.subheader("🔒 Change Password")
            old_pass = st.text_input("Old Password", type='password')
            new_pass = st.text_input("New Password", type='password')

            if st.button("Change"):
                success, message = change_password(st.session_state.username, old_pass, new_pass)
                if success:
                    st.success(message)
                else:
                    st.error(message)

        elif menu_option == "Prediction History":
            st.subheader("📜 Prediction History")
            history = get_user_predictions(st.session_state.username)
            if history:
                for record in history:
                    id, service, date, inputs, result = record
                    with st.expander(f"{date} - {service}"):
                        st.markdown(f"**Inputs:** {inputs}")
                        st.markdown(f"**Result:** {result}")
                        if st.button("Delete", key=f"del_{id}"):
                            delete_prediction(id)
                            st.success("Deleted successfully.")
                            st.rerun()
            else:
                st.info("No prediction history found.")

        elif menu_option == "Help":
            st.info("""
            ### ❓ Help
            - This app allows you to use multiple AI-powered health services.
            - You can predict diabetes, monitor stress, and track your habits.
            - Use the 🏠 menu to manage your profile and account settings.
            """)

        elif menu_option == "Contact Us":
            st.info("""
            ### 📞 Contact Us
            - **Developer**: Sunil Jat  
            - **Email**: technical.programmer.sunil@gmail.com  
            - **Phone**: +91 869-062-5461
            """)

