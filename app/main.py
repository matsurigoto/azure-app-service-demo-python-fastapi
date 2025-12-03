from typing import Union, List
from datetime import date, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DailyWeather(BaseModel):
    date: date
    day_of_week: str
    temperature_high: int
    temperature_low: int
    condition: str
    humidity: int


class WeeklyWeatherResponse(BaseModel):
    city: str
    weekly_forecast: List[DailyWeather]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status}")
def read_root_status():
    return {"Status": "Success"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/weather", response_model=WeeklyWeatherResponse)
async def get_weekly_weather():
    """Get weekly weather forecast for 7 days."""
    today = date.today()
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Simulated weather data for demonstration purposes
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Thunderstorm", "Sunny", "Cloudy"]
    temperatures_high = [28, 26, 24, 25, 27, 29, 30]
    temperatures_low = [22, 21, 20, 19, 21, 23, 24]
    humidity_values = [65, 70, 85, 80, 75, 60, 55]

    weekly_forecast = []
    for i in range(7):
        forecast_date = today + timedelta(days=i)
        weekly_forecast.append(
            DailyWeather(
                date=forecast_date,
                day_of_week=day_names[forecast_date.weekday()],
                temperature_high=temperatures_high[i],
                temperature_low=temperatures_low[i],
                condition=weather_conditions[i],
                humidity=humidity_values[i],
            )
        )

    return WeeklyWeatherResponse(
        city="Taipei",
        weekly_forecast=weekly_forecast,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)