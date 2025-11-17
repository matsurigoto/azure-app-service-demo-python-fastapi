from typing import Union, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import deque

app = FastAPI()

# Data models
class Tutorial(BaseModel):
    id: int
    title: str
    description: str
    url: str

class RecentlyViewedTutorial(BaseModel):
    tutorial_id: int
    title: str
    description: str
    url: str
    viewed_at: datetime

# In-memory storage for tutorials and recently viewed
tutorials_db = {}
recently_viewed_db = {}  # user_id -> deque of viewed tutorials (max 10)

# Initialize with sample tutorials
tutorials_db[1] = Tutorial(id=1, title="Python Basics", description="Learn Python fundamentals", url="https://example.com/python-basics")
tutorials_db[2] = Tutorial(id=2, title="FastAPI Tutorial", description="Build APIs with FastAPI", url="https://example.com/fastapi")
tutorials_db[3] = Tutorial(id=3, title="Docker for Beginners", description="Introduction to Docker", url="https://example.com/docker")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/tutorials", response_model=List[Tutorial])
async def get_tutorials():
    """Get all available tutorials"""
    return list(tutorials_db.values())

@app.get("/tutorials/{tutorial_id}", response_model=Tutorial)
async def get_tutorial(tutorial_id: int):
    """Get a specific tutorial by ID"""
    if tutorial_id not in tutorials_db:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    return tutorials_db[tutorial_id]

@app.post("/tutorials/{tutorial_id}/view")
async def track_tutorial_view(tutorial_id: int, user_id: str = "default_user"):
    """Track when a user views a tutorial"""
    if tutorial_id not in tutorials_db:
        raise HTTPException(status_code=404, detail="Tutorial not found")
    
    tutorial = tutorials_db[tutorial_id]
    
    # Initialize user's recently viewed if not exists
    if user_id not in recently_viewed_db:
        recently_viewed_db[user_id] = deque(maxlen=10)
    
    # Create recently viewed entry using the model
    viewed_entry = RecentlyViewedTutorial(
        tutorial_id=tutorial.id,
        title=tutorial.title,
        description=tutorial.description,
        url=tutorial.url,
        viewed_at=datetime.now()
    )
    
    # Remove if already exists to avoid duplicates (more efficient approach)
    user_views = recently_viewed_db[user_id]
    # Filter out the tutorial if it already exists
    filtered_views = [v for v in user_views if v.tutorial_id != tutorial_id]
    
    # Create new deque with filtered views and add new entry at the front
    recently_viewed_db[user_id] = deque(filtered_views, maxlen=10)
    recently_viewed_db[user_id].appendleft(viewed_entry)
    
    return {"message": "Tutorial view tracked successfully", "tutorial_id": tutorial_id}

@app.get("/tutorials/recently-viewed/list", response_model=List[RecentlyViewedTutorial])
async def get_recently_viewed_tutorials(user_id: str = "default_user"):
    """Get recently viewed tutorials for a user"""
    if user_id not in recently_viewed_db:
        return []
    
    return list(recently_viewed_db[user_id])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
