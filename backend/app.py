from flask import Flask, request
from flask_cors import CORS, cross_origin
import asyncio
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

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
    print("Latitude:", location.latitude)
    print("Longitude:", location.longitude)
    print("Address:", location.address)
    latitude = round(location.latitude, 4)
    longitude = round(location.longitude, 4)

    url = f"https://api.tomorrow.io/v4/weather/realtime?location={latitude}%2C%20{longitude}&apikey=a2qFNOmKYZWIkdNsdewmpgi2x7wxjbKS"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    print(response.text)
    return {'weather': 'success'}
  else:
    print("Location not found.")

  return {'weather': 'fail'}


if __name__ == '__main__':
  app.run(debug=True)