# Assignment_2

[![fastapi-ci](https://github.com/BigDataIA-Spring2023-Team-09/Assignment_2/actions/workflows/fastapi.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-09/Assignment_2/actions/workflows/fastapi.yml)

# Introduction
This project builds up on the Assignment-1 deliverables in which we built a data exploration tool that leverages publicly available data from NOAA website, and the NexRad, GOES satellite datasets. In this project we decoupled the front-end and back-end server functionalities. We used Streamlit framework for designing the front-end application and FastAPI framework to manage the server-side funtionalities. FastAPI is used to handle all the logical and file transfer operations, and communicating respective response status to the Streamlit micro-service. Then, we dockerized both these micro-services and created Airflow DAGs for the same. Using Docker containers as tasks in Airflow DAGs helps to standardize the environment and improve the reliability and scalability of the overall workflow.

![deployment_architecture_diagram](https://user-images.githubusercontent.com/108916132/221307088-48891074-f798-4fff-9284-4e9af118477c.png)

### Files
* <code>nexrad.py</code> : This file generates the UI using streamlit packages to display various filters for the user to use and fetch the required file from the NexRad public S3 bucket. It also enables the user to enter the name of the required file and provides the user with the URL to download it.
* <code>goes18.py</code> : This file generates the UI using streamlit packages to display various filters for the user to use and fetch the required file from the NOAA GOES 18 public S3 bucket. It also enables the user to enter the name of the required file and provides the user with the URL to download it.
* <code>mapping.py</code>: We scraped the URL https://en.wikipedia.org/wiki/NEXRAD#Operational_locations for radar sites. Stored the location table in <code>SQLite DB</code> and plotted an interactive map using <code>folium</code> package.<br>

### Documentation for detailed explanation:
https://docs.google.com/document/d/1RImm4RsAOlxZyvKpwL9RWaHuR_on8LUgoqhEBmin86o/edit?usp=sharing

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
