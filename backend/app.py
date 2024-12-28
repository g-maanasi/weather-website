from flask import Flask, request
from flask_cors import CORS, cross_origin
import asyncio
import requests
from geopy.geocoders import Nominatim
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

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
  city = weather_data['city']
  region = weather_data['region']
  country = weather_data['country']
  geolocator = Nominatim(user_agent="MyApp")
  
  # Get location details
  location = geolocator.geocode(f"${city}, ${region}, ${country}")

  if location:
    latitude = round(location.latitude, 4)
    longitude = round(location.longitude, 4)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
      "latitude": latitude,
      "longitude": longitude,
      "hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "precipitation", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "wind_speed_10m", "is_day", "sunshine_duration"],
      "temperature_unit": "fahrenheit",
      "wind_speed_unit": "ms",
      "precipitation_unit": "inch",
      "timezone": "America/Chicago"
    }
    responses = openmeteo.weather_api(url, params=params)
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_cloud_cover_low = hourly.Variables(4).ValuesAsNumpy()
    hourly_cloud_cover_mid = hourly.Variables(5).ValuesAsNumpy()
    hourly_cloud_cover_high = hourly.Variables(6).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(7).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(8).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(9).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
      start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
      end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
      freq = pd.Timedelta(seconds = hourly.Interval()),
      inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
    hourly_data["cloud_cover_mid"] = hourly_cloud_cover_mid
    hourly_data["cloud_cover_high"] = hourly_cloud_cover_high
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["is_day"] = hourly_is_day
    hourly_data["sunshine_duration"] = hourly_sunshine_duration

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)

    return {'weather': 'success'}
  else:
    print("Location not found.")

  return {'weather': 'fail'}


if __name__ == '__main__':
  app.run(debug=True)