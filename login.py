import streamlit as st
import sqlite3
import hashlib
import re
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            mobile TEXT,
            email TEXT
        )
    ''')
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("INSERT INTO users (username, password, mobile, email) VALUES (?, ?, ?, ?)",
              (username, hashed, mobile, email))
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

# ---------------------- UI Logic ----------------------

def show_login_signup_page():
    st.title("🔐 Secure Login System")
    create_users_table()

    page = st.radio("Select Option", ["Login", "Sign Up"], horizontal=True)

    if page == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if validate_user(username, password):
                st.success(f"Welcome {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password.")

    elif page == "Sign Up":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')
        mobile = st.text_input("Mobile Number")
        email = st.text_input("Email ID")

        if st.button("Create Account"):
            if not valid_username(new_user):
                st.warning("Username must contain only letters and numbers.")
            elif user_exists(new_user):
                st.warning("Username already exists. Choose another one.")
            elif not valid_password(new_pass):
                st.warning("Password must be at least 8 characters.")
            elif not valid_mobile(mobile):
                st.warning("Enter a valid 10-digit mobile number.")
            elif not valid_email(email):
                st.warning("Enter a valid email address.")
            else:
                add_user(new_user, new_pass, mobile, email)
                st.success("Account created successfully!")

# Don't call show_login_signup_page() here directly
# It should be triggered from app.py based on session_state

