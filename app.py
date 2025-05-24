import streamlit as st
import numpy as np
import pickle
import login
import sqlite3
import os

DB_PATH = '/tmp/users.db'


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
# Session State Init
if "show_menu" not in st.session_state:
    st.session_state.show_menu = False

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

# UI Logic
if not st.session_state.logged_in:
    login.show_login_signup_page()
else:
    st.set_page_config(layout="wide")
    col1, col2 = st.columns([1, 9])
    with col1:
        if st.button("🏠", help="Home Menu"):
            st.session_state.show_menu = not st.session_state.get("show_menu", False)

    with col2:
        st.title("🧠 Diabetes Prediction App")

    # Show Menu
    if st.session_state.get("show_menu", False):
        st.subheader("Menu")
        menu_option = st.radio("", ["View Profile", "Change Password", "Logout", "Help", "Contact Us"], index=0)

            if menu_option == "View Profile":
            st.subheader("👤 View / Update Profile")
            user_data = get_user_data(st.session_state.username)
            new_username = st.text_input("Username", value=user_data[0])
            mobile = st.text_input("Mobile Number", value=user_data[1])
            email = st.text_input("Email ID", value=user_data[2])

            # Profile Photo Upload
            profile_dir = f"profile_photos"
            os.makedirs(profile_dir, exist_ok=True)
            photo_path = os.path.join(profile_dir, f"{st.session_state.username}.png")

            uploaded_photo = st.file_uploader("Upload Profile Photo", type=["png", "jpg", "jpeg"])
            if uploaded_photo is not None:
                with open(photo_path, "wb") as f:
                    f.write(uploaded_photo.read())
                st.success("Profile photo updated successfully!")

            # Display Profile Photo if Exists
            if os.path.exists(photo_path):
                st.image(photo_path, width=150, caption="Profile Photo")

            if st.button("Update Profile"):
                success, message = update_user_profile(st.session_state.username, new_username, mobile, email)
                if success:
                    # Rename photo if username changed
                    if new_username != st.session_state.username:
                        new_photo_path = os.path.join(profile_dir, f"{new_username}.png")
                        os.rename(photo_path, new_photo_path)
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

        elif menu_option == "Logout":
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

        elif menu_option == "Help":
            st.info("""
            ### ❓ Help
            - This app uses a Random Forest model to predict diabetes.
            - Input medical data and click "Predict".
            - Use Home menu to manage your account or logout.
            """)

        elif menu_option == "Contact Us":
            st.info("""
            ### 📞 Contact Us
            - **Developer**: Sunil
            - **Email**: contact@example.com
            - **Phone**: +91-9876543210
            """)

    # Prediction UI
    st.subheader("Enter Medical Information")
    model = pickle.load(open("diabetes_model.pkl", "rb"))

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

        if prediction == 1:
            st.error("❌ Likely to have Diabetes")
        else:
            st.success("✅ Unlikely to have Diabetes")

