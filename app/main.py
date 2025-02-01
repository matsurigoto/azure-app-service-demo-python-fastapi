from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/demo")
def read_root():
    return {"Hello": "this is demo"}

@app.get("/test")
def read_root():
    return {"Hello": "this is test"}
