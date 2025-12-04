import random
from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Classroom(BaseModel):
    id: int
    name: str
    building: str
    capacity: int
    floor: int

# Sample classroom data
CLASSROOMS = [
    Classroom(id=1, name="101", building="A", capacity=30, floor=1),
    Classroom(id=2, name="102", building="A", capacity=25, floor=1),
    Classroom(id=3, name="201", building="A", capacity=40, floor=2),
    Classroom(id=4, name="301", building="B", capacity=50, floor=3),
    Classroom(id=5, name="102", building="B", capacity=35, floor=1),
    Classroom(id=6, name="Lab-1", building="C", capacity=20, floor=1),
    Classroom(id=7, name="Lab-2", building="C", capacity=25, floor=2),
    Classroom(id=8, name="Conference", building="D", capacity=15, floor=1),
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/classroom", response_model=Classroom)
def get_random_classroom():
    """Get a random classroom information"""
    if not CLASSROOMS:
        raise HTTPException(status_code=404, detail="No classrooms available")
    return random.choice(CLASSROOMS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)