from typing import Union
from datetime import date
from fastapi import FastAPI

app = FastAPI()


@app.get("/weather")
def get_weather():
    """Return today's weather information."""
    today = date.today().isoformat()
    return {
        "date": today,
        "temperature": 25,
        "unit": "celsius",
        "description": "晴天",
        "humidity": 60,
        "wind_speed": 10
    }

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)