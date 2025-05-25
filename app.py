import streamlit as st
import numpy as np
import pickle
import login
import sqlite3
import os
from login import create_users_table, ensure_default_admin 
from config import DB_PATH
from storage import create_prediction_table, save_prediction, get_user_predictions, delete_prediction
import services.diabetes as diabetes
import services.stress as stress
import services.habit as habit
from storage import create_complaint_table
from login import is_admin

# Ensure tables exist
create_users_table()    
ensure_default_admin() 
create_complaint_table()
create_prediction_table()
login.create_users_table()

# Load diabetes model
MODEL_PATH = "diabetes_model.pkl"
model = pickle.load(open(MODEL_PATH, "rb"))

# Streamlit settings
st.set_page_config(layout="wide")

# ---------------- Session State Initialization ----------------
for key in ["logged_in", "username", "show_menu", "selected_service"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else "" if key == "username" else False if key == "show_menu" else None

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
    col1, col2, col3, col4 = st.columns([1, 1, 9, 9])
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

    # Service Loaders
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

    # Menu Options
    if st.session_state.show_menu and st.session_state.selected_service is None:
        st.markdown("---")
        
        menu_list = ["View Profile", "Change Password", "Prediction History", "Help", "Contact Us"]
        if is_admin(st.session_state.username):
            menu_list.insert(0, "View Complaints")  # Only admin can see this option
        
        menu_option = st.radio("Select an Option:", menu_list, index=0)

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
                st.success(message) if success else st.error(message)

        elif menu_option == "Change Password":
            st.subheader("🔒 Change Password")
            old_pass = st.text_input("Old Password", type='password')
            new_pass = st.text_input("New Password", type='password')
            if st.button("Change"):
                success, message = change_password(st.session_state.username, old_pass, new_pass)
                st.success(message) if success else st.error(message)

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
            - Use the top menu to select a health service.
            - Use 🏠 to view profile, change password, see history.
            - Your data is securely stored and private.
            """)

        elif menu_option == "Contact Us":
            st.info("""
            ### 📞 Contact Us
            - **Developer**: Sunil Jat  
            - **Email**: technical.programmer.sunil@gmail.com  
            - **Phone**: +91 869-062-5461
            """)

        elif menu_option == "View Complaints" and st.session_state.username == "gotohell":
            st.subheader("📬 All User Complaints")
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT username, complaint FROM complaints ORDER BY ROWID DESC")
            complaints = c.fetchall()
            conn.close()

            if complaints:
                for uname, complaint in complaints:
                    with st.expander(f"👤 {uname}"):
                        st.write(complaint)
            else:
                st.info("No complaints submitted yet.")

    # --------------------- Bottom Complaint Box ---------------------
    st.markdown("---")
    st.subheader("📩 Complaint Box")
    st.info("Note: This is a one-way complaint box. You cannot view submitted complaints.")
    with st.form("complaint_form"):
        complaint_text = st.text_area("Type your complaint here...")
        send = st.form_submit_button("Send")
        if send and complaint_text.strip():
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO complaints (username, complaint) VALUES (?, ?)", (st.session_state.username, complaint_text.strip()))
            conn.commit()
            conn.close()
            st.success("✅ Complaint sent successfully!")
            st.rerun()
