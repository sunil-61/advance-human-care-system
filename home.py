import streamlit as st


def show_home_visit_page():
    st.markdown("<h2 style='text-align: center;'>🏠 Welcome to the Home Page</h2>", unsafe_allow_html=True)

    if os.path.exists("loginphoto.jpeg"):
        st.image("loginphoto.jpeg", use_container_width=True)
    else:
        st.warning("Image not found: loginphoto.jpeg")

