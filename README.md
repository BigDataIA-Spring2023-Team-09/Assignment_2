# Assignment_2

[![fastapi-ci](https://github.com/BigDataIA-Spring2023-Team-09/Assignment_2/actions/workflows/fastapi.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-09/Assignment_2/actions/workflows/fastapi.yml)

# Introduction
This project builds up on the Assignment-1 deliverables in which we built a data exploration tool that leverages publicly available data from NOAA website, and the NexRad, GOES satellite datasets. In this project we decoupled the front-end and back-end server functionalities. We used Streamlit framework for designing the front-end application and FastAPI framework to manage the server-side funtionalities. FastAPI is used to handle all the logical and file transfer operations, and communicating respective response status to the Streamlit micro-service. Then, we dockerized both these micro-services and created Airflow DAGs for the same. Using Docker containers as tasks in Airflow DAGs helps to standardize the environment and improve the reliability and scalability of the overall workflow.

![deployment_architecture_diagram](https://user-images.githubusercontent.com/108916132/221307088-48891074-f798-4fff-9284-4e9af118477c.png)

### Files
* <code>.github/workflows/fastapi.yml</code> : This is the YAML file which is used to define the workflow, which includes the various jobs and steps that need to be executed as part of the automation process.
* <code>docker_streamlit/Home.py</code> : This pyhon script is responsible for user authentication using JWT token and serves as the landing page of our application. Streamlit webapp makes RestAPI calls to the FastAPI backend service for any user action.
* <code>docker_streamlit/pages/nexrad.py</code> : This file generates the UI using streamlit packages to display various filters for the user to use and fetch the required file from the NexRad public S3 bucket. It also enables the user to enter the name of the required file and provides the user with the URL to download it.
* <code>docker_streamlit/pages/goes18.py</code> : This file generates the UI using streamlit packages to display various filters for the user to use and fetch the required file from the NOAA GOES 18 public S3 bucket. It also enables the user to enter the name of the required file and provides the user with the URL to download it.
* <code>docker_streamlit/pages/mapping.py</code> : We scraped the URL https://en.wikipedia.org/wiki/NEXRAD#Operational_locations for radar sites. Stored the location table in <code>SQLite DB</code> and plotted an interactive map using <code>folium</code> package.<br>
* <code>fastapi/base_model.py</code> : This file defines a set of Pydantic models that are used for data validation and serialization/deserialization in our Python application. Specifically, it defines models for a token, token data, user, and login credentials, each of which has specific fields with defined data types.
* <code>fastapi/basic_func.py</code> : This file contains all the methods which are required to perform respective ETL tasks. When a specific API call is made, the respective method is called to perform computation in an organized manner.
* <code>fastapi/main.py</code> : This file defines a FastAPI app with several endpoints that use Pydantic models to validate input data and return responses. The code uses several dependencies, including the dotenv library for loading environment variables, the boto3 library for interacting with Amazon S3, and the passlib library for hashing passwords.
* <code>fastapi/test_main.py</code> : This is a test file that tests the endpoints of a FastAPI application. The TestClient is imported from fastapi.testclient and the app instance is imported from main. This file is utilized to implement Continuous Integration using GitHub Actions.
* <code>architecture.py</code> : This script is used to generate the architecture diagram for our application by using the 'diagrams' python module.

### Documentation for detailed explanation:
https://codelabs-preview.appspot.com/?file_id=1QoOS-hG-6P2K4d-iLgIyLbFDi6EW6gLxXD5YU-UdKAM#8

### Application public link:
http://34.74.233.133:8000

### Code review test report:
https://damg-test.s3.amazonaws.com/Testing+/Code+Review+of+Assignment+1+%E2%80%93+Team+8++(1).docx

### End user test report:
https://damg-test.s3.amazonaws.com/Testing+/Enduser+testing+-+Team+11.xlsx

### Attestation:
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
Contribution:
* Ananthakrishnan Harikumar: 25%
* Harshit Mittal: 25%
* Lakshman Raaj Senthil Nathan: 25%
* Sruthi Bhaskar: 25%
