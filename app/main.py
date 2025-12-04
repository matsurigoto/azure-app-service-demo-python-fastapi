from typing import Union, List
from datetime import date, timedelta
from fastapi import FastAPI
from pydantic import BaseModel


class DailyWeather(BaseModel):
    date: date
    temperature_high: float
    temperature_low: float
    condition: str
    humidity: int
    precipitation_chance: int


class WeatherForecast(BaseModel):
    location: str
    forecast: List[DailyWeather]


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/weather", response_model=WeatherForecast)
def get_two_week_weather(location: str = "Taipei"):
    """
    Get two weeks (14 days) weather forecast.
    Returns daily weather data including temperature, condition, humidity, and precipitation chance.
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Overcast"]
    today = date.today()
    forecast = []

    for i in range(14):
        forecast_date = today + timedelta(days=i)
        daily = DailyWeather(
            date=forecast_date,
            temperature_high=25.0 + (i % 5),
            temperature_low=18.0 + (i % 3),
            condition=conditions[i % len(conditions)],
            humidity=60 + (i % 20),
            precipitation_chance=10 + (i % 50)
        )
        forecast.append(daily)

    return WeatherForecast(location=location, forecast=forecast)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)