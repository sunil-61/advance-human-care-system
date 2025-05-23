import streamlit as st
import sqlite3
import hashlib
import re

# ----------------------------- #
# DB setup
conn = sqlite3.connect('users.db')
c = conn.cursor()

def create_users_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')

def add_user(username, password):
    hashed = hash_password(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()

def validate_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    return c.fetchone()

# ----------------------------- #
# Security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def valid_username(username):
    return re.match("^[A-Za-z0-9]+$", username)

def valid_password(password):
    return len(password) >= 8

# ----------------------------- #
# UI
st.title("🔐 Login or Sign Up")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

create_users_table()

if menu == "Sign Up":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type='password')

    if st.button("Create Account"):
        if not valid_username(new_user):
            st.warning("Username must contain only letters and numbers.")
        elif not valid_password(new_pass):
            st.warning("Password must be at least 8 characters.")
        else:
            add_user(new_user, new_pass)
            st.success("Account created successfully!")

elif menu == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        user = validate_user(username, password)
        if user:
            st.success(f"Welcome {username}!")
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password.")

