from flask import Flask, request
from flask_cors import CORS, cross_origin
import asyncio
import requests
from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
@app.route("/")
def hello_world():
  return {"message":"hello world"}

@app.route("/all_countries", methods=["GET"])
@cross_origin(origin='http://localhost:3000')
def get_all_countries_list():
  url = "https://countriesnow.space/api/v0.1/countries/iso"
  response = requests.request("GET", url, headers={}, data={})

  country_list = []
  id = 0
  if response.status_code == 200:
    data = response.json()
    
    for country in data['data']:
      country_list.append({'label': country['name'], 'id': id})
      id += 1
    
    return {'countries': country_list}
  return {}

@app.route("/all_country_regions/<country>", methods=["GET"])
def get_all_regions_from_country(country: str):
  if country == 'Gambia':
    country = 'Gambia The'

  url = "https://countriesnow.space/api/v0.1/countries/states"

  payload = {"country": country}
  response = requests.request("POST", url, headers={}, data=payload)
  
  print(response)
  if response.status_code == 200:
    data = response.json()
    region_list = []

    id = 0
    if response.status_code == 200:
      data = response.json()
      for region in data['data']['states']:
        region_list.append({'label': region['name'], 'id': id})
        id += 1
    
    return {'regions': region_list}
  return {}

@app.route("/all_region_cities/<selection>", methods=["GET"])
def get_all_cities_from_region(selection: str):
  selection_list = selection.split(",")
  url = "https://countriesnow.space/api/v0.1/countries/state/cities"
  payload = {'country': selection_list[0], 'state': selection_list[1]}
  headers = {}

  response = requests.request("POST", url, headers=headers, data=payload)

  if response.status_code == 200:
    data = response.json()
    city_list = []
    id = 0

    if response.status_code == 200:
      data = response.json()
      for city in data['data']:
        city_list.append({'label': city, 'id': id})
        id += 1
    
    return {'cities': city_list}

  return {}

@app.route("/all_country_cities/<country>", methods=["GET"])
def get_all_cities_from_country(country: str):
  payload = {'country': country}
  city_list = []
  id = 0
  response = requests.post("https://countriesnow.space/api/v0.1/countries/cities", json=payload)
  if response.status_code == 200:
    data = response.json()

    for city in data['data']:
        city_list.append({'label': city, 'id': id})
        id += 1
    
    return {'cities': city_list}
  return {}

@app.route("/get_weather", methods=['POST'])
def get_weather_from_city():
  weather_data = dict(request.get_json())
  geolocator = Nominatim(user_agent="MyApp")
  location = ''
  
  # Get location details
  if 'region' in weather_data:
    city = weather_data['city']
    region = weather_data['region']
    country = weather_data['country']
    location = geolocator.geocode(f"${city}, ${region}, ${country}")
  else:
    city = weather_data['city']
    country = weather_data['country']
    location = geolocator.geocode(f"${city}, ${country}")

  if location:
    latitude = round(location.latitude, 4)
    longitude = round(location.longitude, 4)

    # Get the current, hourly, and daily data for the specified location from Open Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
      "latitude": latitude,
      "longitude": longitude,
      "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "cloud_cover", "wind_speed_10m"],
      "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "precipitation", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "wind_speed_10m", "is_day", "sunshine_duration"],
      "daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "precipitation_probability_max"],
      "temperature_unit": "fahrenheit",
      "wind_speed_unit": "ms",
      "precipitation_unit": "inch",
      "timezone": "America/Chicago"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Store the current weather data for today
    current_data = data['current']

    # Get the time range for the hourly weather data
    current_time = datetime.now().strftime("%Y-%m-%dT%H:00")
    end_time = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:00")

    hourly_data = {}
    # Store the hourly data into a dictionary
    for i, time in enumerate(data["hourly"]["time"]):
      if end_time >= time >= current_time:
        hourly_data[time] = {}
        hourly_data[time]["temperature_2m"] = data["hourly"]["temperature_2m"][i]
        hourly_data[time]["apparent_temperature"] = data["hourly"]["apparent_temperature"][i]
        hourly_data[time]["precipitation_probability"] = data["hourly"]["precipitation_probability"][i]
        hourly_data[time]["precipitation"] = data["hourly"]["precipitation"][i]
        hourly_data[time]["cloud_cover_low"] = data["hourly"]["cloud_cover_low"][i]
        hourly_data[time]["cloud_cover_mid"] = data["hourly"]["cloud_cover_mid"][i]
        hourly_data[time]["cloud_cover_high"] = data["hourly"]["cloud_cover_high"][i]
        hourly_data[time]["wind_speed_10m"] = data["hourly"]["wind_speed_10m"][i]
        hourly_data[time]["is_day"] = data["hourly"]["is_day"][i]
        hourly_data[time]["sunshine_duration"] = data["hourly"]["sunshine_duration"][i]

    daily_data = {}
    # Get the daily weather forecast for the specifed location
    for i, time in enumerate(data["daily"]["time"]):
      daily_data[time] = {}
      daily_data[time]['temperature_2m_max'] = data['daily']['temperature_2m_max'][i]
      daily_data[time]['temperature_2m_min'] = data['daily']['temperature_2m_min'][i]
      daily_data[time]['apparent_temperature_max'] = data['daily']['apparent_temperature_max'][i]
      daily_data[time]['apparent_temperature_min'] = data['daily']['apparent_temperature_min'][i]
      daily_data[time]['sunrise'] = data['daily']['sunrise'][i]
      daily_data[time]['sunset'] = data['daily']['sunset'][i]
      daily_data[time]['daylight_duration'] = data['daily']['daylight_duration'][i]
      daily_data[time]['precipitation_probability_max'] = data['daily']['precipitation_probability_max'][i]
    
    return {'weather': 200, 'current': current_data, 'hourly': hourly_data, 'daily': daily_data}
  else:
    print("Location not found.")

  return {'weather': 'fail'}


if __name__ == '__main__':
  app.run(debug=True)