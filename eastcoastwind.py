import streamlit as st
import requests
from datetime import datetime, timedelta

def get_wind_speed(station_id, station_name, date_time):
    url = "https://api-open.data.gov.sg/v2/real-time/api/wind-speed"
    params = {
        "date": date_time
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        readings = data.get('data', {}).get('readings', [])
        for reading in readings:
            for station_data in reading.get('data', []):
                if station_data.get('stationId') == station_id:
                    wind_speed_knots = station_data.get("value")
                    wind_speed_mps = wind_speed_knots * 0.514444  # Convert knots to m/s
                    return {
                        "station_name": station_name,
                        "timestamp": reading.get("timestamp"),
                        "wind_speed": wind_speed_mps,
                        "unit": "m/s"
                    }
    return None

def convert_to_singapore_time(utc_timestamp):
    utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
    singapore_time = utc_time + timedelta(hours=8)
    return singapore_time.strftime("%Y-%m-%d %H:%M:%S")

st.title("Real-time Wind Speed Data")

station_id = "S107"
station_name = "East Coast Parkway"
current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
date_time = st.text_input("Enter the date and time (YYYY-MM-DDTHH:MM:SS)", value=current_time)

if st.button("Get Wind Speed"):
    wind_speed_data = get_wind_speed(station_id, station_name, date_time)
    if wind_speed_data:
        singapore_time = convert_to_singapore_time(wind_speed_data['timestamp'])
        st.write(f"**Wind speed at {wind_speed_data['station_name']} (Station ID: {station_id})**")
        st.write(f"**Timestamp (SGT):** {singapore_time}")
        st.write(f"**Wind Speed:** {wind_speed_data['wind_speed']} {wind_speed_data['unit']}")
    else:
        st.write("No data found for the specified station and time.")
