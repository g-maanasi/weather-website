from flask import Flask
from flask_cors import CORS, cross_origin
import python_weather
import asyncio

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
@cross_origin()
def hello_world():
    asyncio.run(getweather())
    return {"message":"hello world"}


if __name__ == '__main__':
    app.run(debug=True)