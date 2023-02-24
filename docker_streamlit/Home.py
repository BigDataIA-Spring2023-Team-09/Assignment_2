import streamlit as st
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
import sqlite3
import hashlib
from requests.exceptions import HTTPError
import time

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

if "access_token" not in st.experimental_get_query_params() or st.experimental_get_query_params()["access_token"][0]=="None":
        st.session_state.disable_login = False
        st.session_state.logged_in = False
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

    logtxtbox = st.empty()

    if "access_token" in st.experimental_get_query_params():
        # Set up the headers for authenticated requests
        headers = {
            "Authorization": f"Bearer {st.experimental_get_query_params()['access_token'][0]}"
        }
        # Set up the endpoint URL for authenticated requests
        user_info_url = "http://fastapi:8080/users/me"
        # Send a GET request to the user info endpoint to get the user's information
        try:
            response = requests.get(user_info_url, headers=headers)
            response.raise_for_status()
            user_info = response.json()
            # Display the user's information
            logtxtbox.text(f"Welcome {user_info['full_name']}, you are already logged-in!")
            st.session_state.username = user_info['username']
            st.session_state.disable_login=True

        except HTTPError:
            st.session_state.username = ''
            # Get the current query parameters
            query_params = st.experimental_get_query_params()

            # Remove the "access_token" parameter
            query_params["access_token"] = None

            # Set the updated query parameters
            st.experimental_set_query_params(**query_params)
        except Exception as error:
            st.error(f"Error: {error}")
        st.session_state.disable_logout = False

    if login_button:
        st.session_state.username = username
        st.session_state.password = password
        url = "http://fastapi:8080/token"
        json_data = {"username": st.session_state.username, "password": st.session_state.password}

        response = requests.post(url,json=json_data)        
        if response.status_code == 200:
            st.success("Logged in as {}".format(username))

            access_token = response.json()["access_token"]
            st.session_state["access_token"] = access_token

            st.experimental_set_query_params(access_token=st.session_state.access_token)
            
            st.session_state.disable_login = True
            st.session_state.logged_in = True
            st.session_state.disable_logout = False
        else:
            st.error("Invalid username or password")

    with st.sidebar:
        if logout_button:
            for key in st.session_state.keys():
                if (key == 'disable_login' or key == 'disable_logout'):
                    st.session_state[key] = not st.session_state[key]
                else:
                    st.session_state[key] = ''
            st.session_state.disable_login = False
            st.session_state.username = ''
            # Get the current query parameters
            query_params = st.experimental_get_query_params()

            # Remove the "access_token" parameter
            query_params["access_token"] = None

            # Set the updated query parameters
            st.experimental_set_query_params(**query_params)

            logtxtbox.text("")
    
        if "access_token" in st.experimental_get_query_params() and st.experimental_get_query_params()["access_token"][0]!="None":
            st.write(f'Welcome: {st.session_state.username}')
        else:
            st.write('Guest user')
    
def main():
    if login():
        st.write("Kindly continue to explore dashboard from left menu pane!")

if __name__ == "__main__":
    main()