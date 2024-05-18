import requests
from datetime import datetime
import streamlit as st
import pytz
import pandas as pd
import streamlit.components.v1 as components

# Define the Singapore timezone
singapore_tz = pytz.timezone('Asia/Singapore')

# Carpark details
carpark_details = {
    'TM44': 'Blk 499 Tampines Ave 9',
    'T79': 'Blk 460 Tampines St 42',
    'TM12': 'Blk 390A Tampines Ave 7'
}

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
                        'block_number': carpark_details[carpark['carpark_number']],
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
st.header("Carparks near TemaseK JC")

# List of carparks to monitor
carparks_to_monitor = ['TM44', 'T79', 'TM12']

# Get availability data upon loading
carpark_data = get_carpark_availability(carparks_to_monitor)
if isinstance(carpark_data, list):
    # Create a DataFrame for the table
    rows = []
    for carpark in carpark_data:
        for lot in carpark['lots_available']:
            rows.append({
                'Carpark Number': carpark['carpark_number'],
                'Block Number': carpark['block_number'],
                'Update Time': carpark['update_datetime'],
                'Lot Type': lot['lot_type'],
                'Total Lots': lot['total_lots'],
                'Lots Available': lot['lots_available']
            })
    df = pd.DataFrame(rows)
    df.index = df.index + 1  # Set index to start from 1
    st.table(df)
else:
    st.write(carpark_data)


# Embed Google Maps iframe
map_iframe = """
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3988.6988590155843!2d103.9536105768848!3d1.3572997615478641!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31da22b7b378525b%3A0xb349c60aceb7e7e5!2sTemasek%20Junior%20College!5e0!3m2!1sen!2ssg!4v1716004031153!5m2!1sen!2ssg" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
"""
components.html(map_iframe, height=450)

st.write("Check carpark no. using https://services2.hdb.gov.sg/webapp/BN22AWCarParkEnqWeb/BN22CpkInfoSearch.jsp")
