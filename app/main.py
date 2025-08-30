from typing import Union
from fastapi import FastAPI
from .routers import students, teachers, employees

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status")
def read_status():
    return {"status": "ok"}

@app.get("/users/me")
def read_users_me():
    return {"user": "me"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(employees.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)