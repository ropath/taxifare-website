import streamlit as st
import requests
from datetime import datetime
import pydeck as pdk

# Page title
st.title("Taxi Fare Prediction")

# User input for ride parameters
st.header("Enter Ride Details")

# Date and time input
ride_date = st.date_input("Date of ride")
ride_time = st.time_input("Time of ride")

# Convert date and time to a datetime object
ride_datetime = datetime.combine(ride_date, ride_time)

# Pickup and dropoff coordinates input with a map
pickup_longitude = st.number_input("Pickup Longitude", format="%.6f", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", format="%.6f", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", format="%.6f", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", format="%.6f", value=40.748817)

# Passenger count input
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, step=1)

# Displaying the map with Mapbox
st.header("Map View")
midpoint = {
    'latitude': (pickup_latitude + dropoff_latitude) / 2,
    'longitude': (pickup_longitude + dropoff_longitude) / 2
}
# Pydeck map with pickup and dropoff points
map_data = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=midpoint['latitude'],
        longitude=midpoint['longitude'],
        zoom=12,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=[{'lat': pickup_latitude, 'lon': pickup_longitude}, {'lat': dropoff_latitude, 'lon': dropoff_longitude}],
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
)
st.pydeck_chart(map_data)

# API URL
url = 'https://taxifare.lewagon.ai/predict'

# Prepare the parameters for the API request
params = {
    "pickup_datetime": ride_datetime.strftime("%Y-%m-%d %H:%M:%S"),
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# Button to call API and retrieve prediction
if st.button("Predict Fare"):
    try:
        # Call the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        fare = response.json().get("fare", "No fare returned")

        # Display the prediction
        st.success(f"Estimated Fare: ${fare:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
