import streamlit as st
import requests

st.title("Welcome to NOAA dashboard!")

session_state = st.session_state
if "logged_in" not in session_state:
    session_state.logged_in = False

menu = ["Home", "Login"]

session_state = st.session_state

session_state.choice = st.sidebar.selectbox("Select an option", menu)

if session_state.choice == "Home":
    st.subheader("Home")
    st.write("Welcome to NOAA dashboard!")
    
elif session_state.choice == "Login":
    if session_state.logged_in:
        st.warning("You are already logged in.")
    else:
        st.subheader("Login")
        email = st.text_input("email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            payload = {
                "choice": "Login",
                "email": email,
                "password": password
            }
            response = requests.post("http://localhost:8000/landing_page", json=payload)
            result = response.json()
            if "success" in result:
                session_state.logged_in = True
                st.success(result["success"])
            elif "warning" in result:
                st.warning(result["warning"])