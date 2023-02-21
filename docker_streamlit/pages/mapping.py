import folium
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
from pathlib import Path
import streamlit as st

# To facilitate folium support with streamlit package
import streamlit_folium as stf

#To suppress future warnings in python pandas package
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

st.header(':blue[Operational locations of NEXRAD sites]')

with st.spinner('Refreshing map...'):
    requests.get("http://localhost:8000/mapping-stations")

