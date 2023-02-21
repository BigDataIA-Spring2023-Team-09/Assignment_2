import pandas as pd
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

url="https://en.wikipedia.org/wiki/NEXRAD#Operational_locations"
response=requests.get(url)
soup=BeautifulSoup(response.text, 'html.parser')
tables=soup.find_all("table")
for index, table in enumerate(tables):
    if ("List of NEXRAD sites and their coordinates" in str(table)):
        table_index = index

data = pd.DataFrame(columns=["State", "City", "Identifier", "Coordinates"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        state = col[0].text
        city = col[1].text
        identifier = col[2].text
        coordinates = col[3].text
        data = data.append({"State":state, "City":city, "Identifier":identifier, "Coordinates":coordinates}, ignore_index=True)

#Performing computations to extract latitude and longitude values from 'Coordinates' column
def transformCol(x):
    return x.split("/")[2].split("\ufeff")[0].replace(";",",").lstrip()

data['Coordinates']=data['Coordinates'].apply(transformCol)

df=pd.DataFrame(columns=['lat', 'long'])
for i in data['Coordinates']:
    lati=float(i.split(",")[0])
    longi=float(i.split(",")[1].rstrip())
    df=df.append({'lat':lati, 'long':longi}, ignore_index=True)

final_df=pd.concat([data, df], axis=1)

database_file_name = 'location.db'
ddl_file_name = 'ddl.sql'
database_file_path = os.path.join(os.path.dirname(__file__),database_file_name)
ddl_file_path = os.path.join(os.path.dirname(__file__),ddl_file_name)

def create_database():
    with open(ddl_file_path, 'r') as sql_file:
        sql_script = sql_file.read()
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

def check_database_initilization():
    #print(os.path.dirname(__file__))
    if not Path(database_file_path).is_file():
        create_database()
    # else:
    #     print("Database file already exist")

def write_to_db(final_df):
    db = sqlite3.connect(database_file_path)
    final_df.to_sql(name='loaction_radar', con=db, if_exists='replace', index=False)
    db.commit()
    db.close()
    del final_df

#Reading the respective location features from DB and creating circle markers, pop-up markers for each
def read_from_db():
    latitudes=[]
    longitudes=[]
    labels=[]
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()
    sat_data=cursor.execute('''SELECT lat, long, City FROM loaction_radar''')
    satellite = folium.map.FeatureGroup()
    for record in sat_data:
        satellite.add_child(
                folium.features.CircleMarker(
                    [record[0], record[1]],
                    radius=5, # define how big you want the circle markers to be
                    color='yellow',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.6
                )
            )
        latitudes.append(record[0])
        longitudes.append(record[1])
        labels.append(record[2])
    
    # create map with a default starting location
    satellite_map = folium.Map(location=[37.6, -95.665], zoom_start=3)

    # add pop-up text to each marker on the map
    for lat, lng, label in zip(latitudes, longitudes, labels):
        folium.Marker([lat, lng], popup=label).add_to(satellite_map)    

    # add satellite to map and display it using streamlit-folium package
    satellite_map.add_child(satellite)
    stf.st_folium(satellite_map, width=700, height=460)
    st.text("Click on marker to view city name!")

def main():
    check_database_initilization()
    write_to_db(final_df)
    with st.spinner('Refreshing map...'):
        read_from_db()

if __name__ == "__main__":
    main()
    del final_df