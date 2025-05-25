import streamlit as st
import sqlite3

def view_complaints():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT username, complaint, timestamp FROM complaints ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    
    st.title("📋 All Complaints")
    if data:
        for i, (user, complaint, time) in enumerate(data, 1):
            st.markdown(f"**{i}. User:** `{user}` | 🕒 `{time}`")
            st.markdown(f"```\n{complaint}\n```")
            st.markdown("---")
    else:
        st.info("No complaints submitted yet.")

