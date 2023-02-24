import requests
import streamlit as st
import os
from requests.exceptions import HTTPError
import time

if 'username' not in st.session_state:
    st.session_state.username = ''

if "access_token" in st.experimental_get_query_params() and st.experimental_get_query_params()["access_token"][0]!="None":
    st.markdown("<h1 style='text-align: center;'>NEXRAD</h1>", unsafe_allow_html=True)
    st.header("")
    st.header("Search by Fields")
    st.header("")


    BASE_URL = "http://fastapi:8080"


    col1, col2, col3, col4 = st.columns(4, gap="large")


    # Make a request to the endpoint to retrieve the list of years
    year_response = (requests.get(BASE_URL + '/list-years-nexrad')).json()
    year_list = year_response["year_list"]


    with col1:
        year = st.selectbox(
            'Select the Year :',
            (year_list))
        st.write('You selected :', year)


    # Make a request to the endpoint to retrieve the list of months for the selected year
    month_response = requests.post(BASE_URL + f'/list-months-nexrad?year={year}').json()
    month_list = month_response["month_list"]

    
    with col2:
        month = st.selectbox(
            'Select the Month :',
            (month_list))

        st.write('You selected :', month)


    # Make a request to the endpoint to retrieve the list of days for the selected year and month
    day_response = requests.post(BASE_URL + f'/list-days-nexrad?year={year}&month={month}').json()
    day_list = day_response["days_list"]


    with col3:
        day = st.selectbox(
            'Select the Date :',
            (day_list))

        st.write('You selected :', day)


    # Make a request to the endpoint to retrieve the list of stations for the selected year and day
    station_response = (requests.post(BASE_URL + f'/list-stations-nexrad?year={year}&month={month}&day={day}')).json()
    station_list = station_response['stations_list']


    with col4:

        station = st.selectbox(
            'Select the Station :',
            (station_list))

        st.write('You selected :', station)


    st.header("")


    # Make a request to the endpoint to retrieve the list of files for the selected year, day
    file_list_response = (requests.post(BASE_URL + f'/list-files-nexrad?year={year}&month={month}&day={day}&station={station}')).json()
    file_list = file_list_response["file_list"]


    selected_file = st.selectbox("Select link for download", 
                (file_list),  
                key=None, help="select link for download")


    st.header("")


    if st.button('Generate using Filter'):

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
            # logtxtbox.text(f"Welcome {user_info['full_name']}, you are already logged-in!")
            st.session_state.username = user_info['username']
            st.session_state.disable_login=True
           
            # Make a request to the endpoint to fetch the url for the selected file
            file_url_response = requests.post(BASE_URL + f'/fetch-url-nexrad?name={selected_file}').json()
            file_url = file_url_response["url"]

            # Display the url for the selected file
            st.write('Download Link : ', file_url)

            # Make a request to the endpoint to fetch the url for the selected file from the Nexrad bucket for validation
            validation_url_response = requests.post(BASE_URL + f'/validate-url-nexrad?name={selected_file}').json()
            validation_url = validation_url_response["url"]
            
            st.write("NOAA bucket path for verfication : ", validation_url)

        except HTTPError:
            st.session_state.username = ''
            # Get the current query parameters
            query_params = st.experimental_get_query_params()

            # Remove the "access_token" parameter
            query_params["access_token"] = None

            # Set the updated query parameters
            st.experimental_set_query_params(**query_params)
            st.text("Session timed-out, please login again!")
        except Exception as error:
            st.error(f"Error: {error}")
        st.session_state.disable_logout = False


    st.header("")
    st.header("Search by Filename")
    st.header("")


    filename = st.text_input('Enter Filename')
    st.header("")



    if st.button('Generate using Name'):

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
            # logtxtbox.text(f"Welcome {user_info['full_name']}, you are already logged-in!")
            st.session_state.username = user_info['username']
            st.session_state.disable_login=True

            # Copies the file from Nexrad bucket to User bucket and generates download URL
            file_url_response = requests.post(BASE_URL + f'/fetch-url-nexrad-from-name?name={filename}').json()
            file_url = file_url_response["url"]    

            # Display the url for the selected file
            st.write('Download Link : ', file_url)

        except HTTPError:
            st.session_state.username = ''
            # Get the current query parameters
            query_params = st.experimental_get_query_params()

            # Remove the "access_token" parameter
            query_params["access_token"] = None

            # Set the updated query parameters
            st.experimental_set_query_params(**query_params)
            st.text("Session timed-out, please login again!")
        except Exception as error:
            st.error(f"Error: {error}")
        st.session_state.disable_logout = False

else:
    st.title("Please sign-in to access this feature!")