import streamlit as st
import sqlite3

def view_complaints():
    st.title("📋 All Complaints")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, complaint, timestamp FROM complaints ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    if rows:
        for i, (user, comp, time) in enumerate(rows, 1):
            st.markdown(f"**{i}.** 👤 `{user}` | 🕒 `{time}`")
            st.code(comp)
            st.markdown("---")
    else:
        st.info("No complaints submitted yet.")


