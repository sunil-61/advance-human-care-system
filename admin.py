import streamlit as st
import sqlite3

def view_feedbacks():
    st.title("📋 All feedbacks")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, feedback, timestamp FROM feedbacks ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    if rows:
        for i, (user, comp, time) in enumerate(rows, 1):
            st.markdown(f"**{i}.** 👤 `{user}` | 🕒 `{time}`")
            st.code(comp)
            st.markdown("---")
    else:
        st.info("No feedbacks submitted yet.")


