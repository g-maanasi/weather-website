from flask import Flask
from flask_cors import CORS, cross_origin
import python_weather
import asyncio
import requests

app = Flask(__name__)
CORS(app)

async def getweather() -> None:
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get('New York')
    
    # returns the current day's forecast temperature (int)
    print(weather.temperature)
    
    # get the weather forecast for a few days
    for daily in weather:
      print(daily)
      
      # hourly forecasts
      for hourly in daily:
        print(f' --> {hourly!r}')

@app.route("/")
def hello_world():
  asyncio.run(getweather())
  return {"message":"hello world"}

@app.route("/all_countries", methods=["GET"])
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
  payload = str(payload)
  response = requests.request("POST", url, headers={}, data=payload)
  
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

if __name__ == '__main__':
  app.run(debug=True)