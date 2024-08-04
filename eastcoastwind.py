import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

def get_wind_speed(station_id, station_name, date_time):
    url = "https://api-open.data.gov.sg/v2/real-time/api/wind-speed"
    params = {
        "date": date_time
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        readings = data.get('data', {}).get('readings', [])
        wind_speed_data = []
        for reading in readings:
            for station_data in reading.get('data', []):
                if station_data.get('stationId') == station_id:
                    wind_speed_knots = station_data.get("value")
                    wind_speed_mps = wind_speed_knots * 0.514444  # Convert knots to m/s
                    wind_speed_data.append({
                        "timestamp": reading.get("timestamp"),
                        "wind_speed": wind_speed_mps
                    })
        return wind_speed_data
    return None

def convert_to_singapore_time(utc_timestamp):
    utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
    singapore_time = utc_time + timedelta(hours=8)
    return singapore_time.strftime("%Y-%m-%d %H:%M:%S")

st.title("Real-time Wind Speed Data for the Last 6 Hours")

station_id = "S107"
station_name = "East Coast Parkway"
current_time_sgt = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=6)
interval = timedelta(minutes=10)

date_times = [start_time + i*interval for i in range(int((end_time - start_time) / interval) + 1)]
date_times_sgt = [dt + timedelta(hours=8) for dt in date_times]

wind_speed_data_list = []
for dt in date_times:
    date_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
    wind_speed_data = get_wind_speed(station_id, station_name, date_time_iso)
    if wind_speed_data:
        wind_speed_data_list.extend(wind_speed_data)

if wind_speed_data_list:
    for data in wind_speed_data_list:
        data['timestamp'] = convert_to_singapore_time(data['timestamp'])
    df = pd.DataFrame(wind_speed_data_list)
    df = df.drop_duplicates(subset=['timestamp'])
    df = df.sort_values(by='timestamp')
    st.write(f"**Wind speed at {station_name} (Station ID: {station_id}) for the last 6 hours**")
    st.write(df)
else:
    st.write("No data found for the specified station and time intervals.")
