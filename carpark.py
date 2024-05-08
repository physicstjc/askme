import requests
from datetime import datetime

# Function to get the carpark availability for T18
def get_carpark_availability(carpark_number='T18'):
    # Set the API endpoint and headers
    url = 'https://api.data.gov.sg/v1/transport/carpark-availability'
    headers = {'accept': '*/*'}
    
    # Use the current datetime in the format required by the API
    date_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    
    # Define the query parameters
    params = {'date_time': date_time}
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        carpark_data = data['items'][0]['carpark_data']
        
        # Extract the data for the specified carpark number
        for carpark in carpark_data:
            if carpark['carpark_number'] == carpark_number:
                return carpark
        
        return f"No data found for carpark number: {carpark_number}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Example usage
carpark_info = get_carpark_availability('T18')
print(carpark_info)
