import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

def get_wind_data(station_id, station_name, date_time, data_type):
    url = f"https://api-open.data.gov.sg/v2/real-time/api/{data_type}"
    params = {
        "date": date_time
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        readings = data.get('data', {}).get('readings', [])
        wind_data = []
        for reading in readings:
            for station_data in reading.get('data', []):
                if station_data.get('stationId') == station_id:
                    value = station_data.get("value")
                    wind_data.append({
                        "timestamp": reading.get("timestamp"),
                        f"{data_type}": value
                    })
        return wind_data
    return None

def convert_to_singapore_time(utc_timestamp):
    utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
    singapore_time = utc_time + timedelta(hours=8)
    return singapore_time.strftime("%Y-%m-%d %H:%M:%S")

st.title("Real-time Wind Speed and Direction Data for the Last Hour")

station_id = "S107"
station_name = "East Coast Parkway"
current_time_sgt = (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=1)
interval = timedelta(minutes=10)

if st.button("Retrieve Wind Data"):
    date_times = [start_time + i*interval for i in range(int((end_time - start_time) / interval) + 1)]
    wind_speed_data_list = []
    wind_direction_data_list = []

    for dt in date_times:
        date_time_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
        wind_speed_data = get_wind_data(station_id, station_name, date_time_iso, "wind-speed")
        wind_direction_data = get_wind_data(station_id, station_name, date_time_iso, "wind-direction")
        if wind_speed_data:
            wind_speed_data_list.extend(wind_speed_data)
        if wind_direction_data:
            wind_direction_data_list.extend(wind_direction_data)

    if wind_speed_data_list and wind_direction_data_list:
        wind_speed_df = pd.DataFrame(wind_speed_data_list).drop_duplicates(subset=['timestamp']).sort_values(by='timestamp')
        wind_direction_df = pd.DataFrame(wind_direction_data_list).drop_duplicates(subset=['timestamp']).sort_values(by='timestamp')
        
        df = pd.merge(wind_speed_df, wind_direction_df, on="timestamp")
        df['timestamp'] = df['timestamp'].apply(convert_to_singapore_time)
        df.rename(columns={"wind-speed": "Wind Speed (m/s)", "wind-direction": "Wind Direction (degrees)"}, inplace=True)
        
        st.write(f"**Wind speed and direction at {station_name} (Station ID: {station_id}) for the last hour**")
        st.write(df)
    else:
        st.write("No data found for the specified station and time intervals.")
