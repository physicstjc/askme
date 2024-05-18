import requests
from datetime import datetime
import streamlit as st
import pytz
import pandas as pd
import folium
from streamlit_folium import st_folium

# Define the Singapore timezone
singapore_tz = pytz.timezone('Asia/Singapore')

# Function to get the carpark availability for a given list of carpark numbers
def get_carpark_availability(carpark_numbers):
    url = 'https://api.data.gov.sg/v1/transport/carpark-availability'
    headers = {'accept': '*/*'}
    date_time = datetime.now(singapore_tz).strftime('%Y-%m-%dT%H:%M:%S')
    params = {'date_time': date_time}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        carpark_data = data['items'][0]['carpark_data']
        results = []
        
        for carpark_number in carpark_numbers:
            for carpark in carpark_data:
                if carpark['carpark_number'] == carpark_number:
                    carpark_info = {
                        'carpark_number': carpark['carpark_number'],
                        'update_datetime': carpark['update_datetime'],
                        'lots_available': []
                    }
                    for info in carpark['carpark_info']:
                        carpark_info['lots_available'].append({
                            'lot_type': info['lot_type'],
                            'total_lots': info['total_lots'],
                            'lots_available': info['lots_available']
                        })
                    results.append(carpark_info)
                    break
        
        return results
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit app
st.title("HDB Carpark Availability Checker")
st.header("Carparks near TJC")

# List of carparks to monitor
carparks_to_monitor = ['T18', 'TM44', 'T79', 'TM12']

if st.button("Get Availability"):
    carpark_data = get_carpark_availability(carparks_to_monitor)
    if isinstance(carpark_data, list):
        # Create a DataFrame for the table
        rows = []
        for carpark in carpark_data:
            for lot in carpark['lots_available']:
                rows.append({
                    'Carpark Number': carpark['carpark_number'],
                    'Update Time': carpark['update_datetime'],
                    'Lot Type': lot['lot_type'],
                    'Total Lots': lot['total_lots'],
                    'Lots Available': lot['lots_available']
                })
        df = pd.DataFrame(rows)
        st.table(df)
    else:
        st.write(carpark_data)

st.write("Check carpark no. using https://services2.hdb.gov.sg/webapp/BN22AWCarParkEnqWeb/BN22CpkInfoSearch.jsp")

# Add Google Map with Temasek Junior College as the centre
# Coordinates for Temasek Junior College
temasek_jc_coords = [1.3210, 103.9240]

# Create a Folium map
m = folium.Map(location=temasek_jc_coords, zoom_start=16)

# Add a marker for Temasek Junior College
folium.Marker(temasek_jc_coords, popup='Temasek Junior College').add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)
