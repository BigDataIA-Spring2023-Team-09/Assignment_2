import requests
import streamlit as st
from requests.exceptions import HTTPError
import time

if 'username' not in st.session_state:
    st.session_state.username = ''

if "access_token" in st.experimental_get_query_params() and st.experimental_get_query_params()["access_token"][0]!="None":
    st.markdown("<h1 style='text-align: center;'>GOES-18</h1>", unsafe_allow_html=True)
    st.header("")
    st.header("Search by Fields")
    st.header("")


    BASE_URL = "http://fastapi:8090"

    col1, col2, col3 = st.columns(3, gap="large")

    # Make a request to the endpoint to retrieve the list of years
    year_response = (requests.get(BASE_URL + '/list-years-goes')).json()
    year_list = year_response["year_list"]


    with col1:
        year = st.selectbox(
            'Select the Year :',
            (year_list))
        st.write('You selected :', year)


    # Make a request to the endpoint to retrieve the list of days for the selected year
    day_response = requests.post(BASE_URL + f'/list-days-goes?year={year}').json()
    day_list = day_response["days_list"]


    with col2:
        day = st.selectbox(
            'Select the Day :',
            (day_list))
        st.write('You selected :', day)
    

    # Make a request to the endpoint to retrieve the list of hours for the selected year and day
    hour_response = (requests.post(BASE_URL + f'/list-hours-goes?year={year}&day={day}')).json()
    hour_list = hour_response['hours_list']


    with col3:
        hour = st.selectbox(
            'Select the Hour :',
            (hour_list))
        st.write('You selected :', hour)
    st.header("")


    # Make a request to the endpoint to retrieve the list of files for the selected year, day and hour
    file_list_response = (requests.post(BASE_URL + f'/list-files-goes?year={year}&day={day}&hour={hour}')).json()
    file_list = file_list_response["file_list"]


    selected_file = st.selectbox("Select link for download", 
                (file_list),  
                key=None, help="select link for download")


    st.header("")


    if st.button('Generate using Filter'):

        headers = {
            "Authorization": f"Bearer {st.experimental_get_query_params()['access_token'][0]}"
        }
        # Set up the endpoint URL for authenticated requests
        user_info_url = "http://fastapi:8090/users/me"
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
            file_url_response = requests.post(BASE_URL + f'/fetch-url-goes?name={selected_file}').json()
            file_url = file_url_response["url"]

            # Display the url for the selected file
            st.write('Download Link : ', file_url)

            # Make a request to the endpoint to fetch the url for the selected file from the GOES18 bucket for validation
            validation_url_response = requests.post(BASE_URL + f'/validate-url-goes?name={selected_file}').json()
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
        user_info_url = "http://fastapi:8090/users/me"
        # Send a GET request to the user info endpoint to get the user's information
        try:
            response = requests.get(user_info_url, headers=headers)
            response.raise_for_status()
            user_info = response.json()
            # Display the user's information
            # logtxtbox.text(f"Welcome {user_info['full_name']}, you are already logged-in!")
            st.session_state.username = user_info['username']
            st.session_state.disable_login=True

            # Copies the file from GOES18 bucket to User bucket and generates download URL
            file_url_response = requests.post(BASE_URL + f'/fetch-url-goes-from-name?name={filename}').json()
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