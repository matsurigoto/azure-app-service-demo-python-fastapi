import random
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Student data model
class Student(BaseModel):
    id: int
    name: str
    age: int
    grade: str

# Sample student data
STUDENTS = [
    Student(id=1, name="王小明", age=18, grade="A"),
    Student(id=2, name="李小華", age=19, grade="B"),
    Student(id=3, name="張小美", age=17, grade="A"),
    Student(id=4, name="陳小強", age=20, grade="C"),
    Student(id=5, name="林小玲", age=18, grade="B"),
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

@app.get("/students/random", response_model=Student)
def get_random_student():
    """Get a random student's data"""
    return random.choice(STUDENTS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)