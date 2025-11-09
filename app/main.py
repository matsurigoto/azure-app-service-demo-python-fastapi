from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status")
def read_status():
    return {"Status": "Success"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    import uvicorn
    # Bind to 0.0.0.0 for container/cloud deployments (Azure App Service)
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
