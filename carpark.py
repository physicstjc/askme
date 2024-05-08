import requests
from datetime import datetime
import streamlit as st

# Function to get the carpark availability for a given carpark number
def get_carpark_availability(carpark_number='T18'):
    url = 'https://api.data.gov.sg/v1/transport/carpark-availability'
    headers = {'accept': '*/*'}
    date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    params = {'date_time': date_time}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        carpark_data = data['items'][0]['carpark_data']
        
        for carpark in carpark_data:
            if carpark['carpark_number'] == carpark_number:
                return carpark
        
        return f"No data found for carpark number: {carpark_number}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit app
st.title("HDB Carpark Availability Checker")

# Input for carpark number
carpark_number = st.text_input("Enter Carpark Number", "T18")

if st.button("Get Availability"):
    carpark_info = get_carpark_availability(carpark_number)
    if isinstance(carpark_info, dict):
        st.subheader(f"Carpark Number: {carpark_info['carpark_number']}")
        st.write("Last Updated:", carpark_info['update_datetime'])
        
        for info in carpark_info['carpark_info']:
            st.write(f"Lot Type: {info['lot_type']}")
            st.write(f"Total Lots: {info['total_lots']}")
            st.write(f"Lots Available: {info['lots_available']}")
            st.write("---")
    else:
        st.write(carpark_info)
