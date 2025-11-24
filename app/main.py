from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Teacher data model
class Teacher(BaseModel):
    id: int
    name: str
    subject: str
    email: str
    years_of_experience: int = 0

# In-memory storage for teachers
teachers_db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Teacher API endpoints
@app.get("/teachers", response_model=List[Teacher])
async def get_teachers():
    """Get all teachers"""
    return list(teachers_db.values())

@app.get("/teachers/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: int):
    """Get a specific teacher by ID"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teachers_db[teacher_id]

@app.post("/teachers", response_model=Teacher)
async def create_teacher(teacher: Teacher):
    """Create a new teacher"""
    if teacher.id in teachers_db:
        raise HTTPException(status_code=400, detail="Teacher with this ID already exists")
    teachers_db[teacher.id] = teacher
    return teacher

@app.put("/teachers/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: int, teacher: Teacher):
    """Update an existing teacher"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    if teacher.id != teacher_id:
        raise HTTPException(status_code=400, detail="Teacher ID in path and body must match")
    teachers_db[teacher_id] = teacher
    return teacher

@app.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int):
    """Delete a teacher"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    deleted_teacher = teachers_db.pop(teacher_id)
    return {"message": "Teacher deleted successfully", "teacher": deleted_teacher}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)