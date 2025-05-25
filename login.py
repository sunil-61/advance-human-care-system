import streamlit as st
import sqlite3
import hashlib
import re
import os
from config import DB_PATH

# ---------------------- Utility Functions ----------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def valid_username(username):
    return re.match("^[A-Za-z0-9]+$", username)

def valid_password(password):
    return len(password) >= 8

def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def valid_mobile(mobile):
    return re.match(r"^[6-9]\d{9}$", mobile)

# ---------------------- Database Operations ----------------------

def create_users_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        mobile TEXT,
        email TEXT,
        is_admin INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def user_exists(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_user(username, password, mobile, email):
    hashed_pwd = hash_password(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, mobile, email, is_admin) VALUES (?, ?, ?, ?, 0)", 
              (username, hashed_pwd, mobile, email))
    conn.commit()
    conn.close()

def validate_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    result = c.fetchone()
    conn.close()
    return result

def is_admin(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == 1


# ---------------------- UI Logic ----------------------

def show_login_signup_page():
    st.markdown("<h2 style='text-align: center;'>🏥 Welcome to the Advance Health Care System</h2>", unsafe_allow_html=True)

    create_users_table()

    if os.path.exists("loginphoto.jpeg"):
        st.image("loginphoto.jpeg", use_container_width=True)
    else:
        st.warning("Image not found: loginphoto.jpeg")

    if 'mode' not in st.session_state:
        st.session_state.mode = 'login'

    # ------------------- Login Mode ------------------- #
    if st.session_state.mode == 'login':
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        st.write("")  # spacing

        col1, col2, col3 = st.columns([5.6, 2, 5])
        with col2:
            if st.button("Login", key="login_action"):
                if validate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.markdown("<p style='color: orange;'>⚠️ Invalid username or password.</p>", unsafe_allow_html=True)

        col7, col8, col9 = st.columns([5.5, 2, 5])
        with col8:
            if st.button("Create New Account"):
                st.session_state.mode = 'signup'
                st.rerun()

    # ------------------- Sign Up Mode ------------------- #
    elif st.session_state.mode == 'signup':
        st.subheader("Create New Account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type='password')
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email ID")

        if st.button("Create Account"):
            if not valid_username(new_user):
                st.warning("Username must contain only letters and numbers.")
            elif user_exists(new_user):
                st.warning("Username already exists.")
            elif not valid_password(new_pass):
                st.warning("Password must be at least 8 characters.")
            elif not valid_mobile(mobile):
                st.warning("Enter a valid 10-digit mobile number.")
            elif not valid_email(email):
                st.warning("Enter a valid email address.")
            else:
                add_user(new_user, new_pass, mobile, email)
                st.success("Account created successfully! You can now log in.")
                st.session_state.mode = 'login'
                st.rerun()

        st.write("")
        if st.button("Back to Login"):
            st.session_state.mode = 'login'
            st.rerun()

