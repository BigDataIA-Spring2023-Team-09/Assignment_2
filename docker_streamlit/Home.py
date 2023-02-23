import streamlit as st
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import requests
import sqlite3
import hashlib

st.set_page_config(
    page_title="NOAA Dashboard",
    page_icon="👋",
)

if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

if 'username' not in st.session_state:
    st.session_state.username = ''

if 'password' not in st.session_state:
    st.session_state.password = ''

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'disable_login' not in st.session_state:
    st.session_state.disable_login = False

if 'disable_logout' not in st.session_state:
    st.session_state.disable_logout = True

# define the Streamlit login page
def login():
    st.title("Welcome to NOAA dashboard!")
    st.subheader("Existing user? Login below.")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    username = st.text_input ("Username", st.session_state.username, placeholder="Username")
    password = st.text_input ("Password", st.session_state.password, placeholder="Password", type='password')
    login_button = st.button ('Login', disabled = st.session_state.disable_login)
    logout_button = st.button ('LogOut', disabled = st.session_state.disable_logout)

    if login_button:
        st.session_state.username = username
        st.session_state.password = password
        url = "http://localhost:8000/token"
        json_data = {"username": st.session_state.username, "password": st.session_state.password}

        response = requests.post(url,json=json_data)        
        if response.status_code == 200:
            st.success("Logged in as {}".format(username))
            st.session_state.access_token = response.json()['access_token']
            st.session_state.disable_login = True
            st.session_state.logged_in = True
            st.session_state.disable_logout = False
        else:
            st.error("Invalid username or password")
    
    with st.sidebar:
        if (st.session_state.logged_in and st.session_state and st.session_state.username):
            st.write(f'Welcome: {st.session_state.username}')
        else:
            st.write('Guest user')

        if logout_button:
            for key in st.session_state.keys():
                if (key == 'disable_login' or key == 'disable_logout'):
                    st.session_state[key] = not st.session_state[key]
                else:
                    st.session_state[key] = ''
            st.session_state.disable_login = False
    
def main():
    if login():
        st.write("Kindly continue to explore dashboard from left menu pane!")

if __name__ == "__main__":
    main()