import streamlit as st
import sqlite3
import os
import hashlib
import re

# ✅ Cloud-safe database path
DB_PATH = '/tmp/users.db'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def valid_username(username):
    return re.match("^[A-Za-z0-9]+$", username)

def valid_password(password):
    return len(password) >= 8

def create_users_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hashed = hash_password(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
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

def show_login_page():
    st.title("🔐 Login System")
    create_users_table()

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

    st.markdown("---")
    st.subheader("Don't have an account? Sign Up below")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')

    if st.button("Create Account"):
        if not valid_username(new_user):
            st.warning("Username must contain only letters and numbers.")
        elif not valid_password(new_pass):
            st.warning("Password must be at least 8 characters.")
        else:
            add_user(new_user, new_pass)
            st.success("Account created successfully!")

# Run the page
show_login_page()
