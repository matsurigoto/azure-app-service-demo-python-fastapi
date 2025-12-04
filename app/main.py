import random
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Teacher(BaseModel):
    id: int
    name: str
    subject: str
    email: str


# Sample teacher data
TEACHERS = [
    Teacher(id=1, name="王小明", subject="數學", email="wang.xiaoming@school.edu.tw"),
    Teacher(id=2, name="李美華", subject="英文", email="li.meihua@school.edu.tw"),
    Teacher(id=3, name="陳志強", subject="物理", email="chen.zhiqiang@school.edu.tw"),
    Teacher(id=4, name="林雅婷", subject="化學", email="lin.yating@school.edu.tw"),
    Teacher(id=5, name="張偉民", subject="國文", email="zhang.weimin@school.edu.tw"),
]

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status}")
def read_status():
    return {"Status": "Success"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/teacher", response_model=Teacher)
def get_random_teacher():
    """查詢教師 API，回傳隨機一位教師資料"""
    return random.choice(TEACHERS)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)