from typing import Union
from datetime import date, timedelta
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class DailyWeather(BaseModel):
    date: str
    day_of_week: str
    condition: str
    temperature_high: int
    temperature_low: int
    humidity: int


class WeeklyWeatherResponse(BaseModel):
    week_start: str
    week_end: str
    forecast: list[DailyWeather]


def get_weekly_weather() -> WeeklyWeatherResponse:
    """Generate mock weekly weather data."""
    today = date.today()
    conditions = ["晴天", "多雲", "陰天", "小雨", "晴時多雲", "多雲時晴", "雷陣雨"]
    day_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    forecast = []
    for i in range(7):
        current_date = today + timedelta(days=i)
        day_of_week = day_names[current_date.weekday()]
        temp_high = 28 + (i % 5)
        temp_low = min(22 + (i % 3), temp_high - 5)
        humidity = min(60 + (i * 3), 85)
        forecast.append(
            DailyWeather(
                date=current_date.isoformat(),
                day_of_week=day_of_week,
                condition=conditions[i % len(conditions)],
                temperature_high=temp_high,
                temperature_low=temp_low,
                humidity=humidity,
            )
        )
    
    return WeeklyWeatherResponse(
        week_start=today.isoformat(),
        week_end=(today + timedelta(days=6)).isoformat(),
        forecast=forecast,
    )

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/weather")
def get_weather() -> WeeklyWeatherResponse:
    """Get weekly weather forecast. 取得一週天氣預報。"""
    return get_weekly_weather()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)