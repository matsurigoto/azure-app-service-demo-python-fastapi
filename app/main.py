from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Teacher model
class Teacher(BaseModel):
    id: int
    name: str
    subject: str
    email: str
    years_of_experience: Optional[int] = 0

class TeacherCreate(BaseModel):
    name: str
    subject: str
    email: str
    years_of_experience: Optional[int] = 0

class TeacherUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    email: Optional[str] = None
    years_of_experience: Optional[int] = None

# In-memory storage (Note: Not thread-safe. Use database or locks for production)
teachers_db = {}
teacher_id_counter = 1

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status")
def read_status():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Teacher API endpoints
@app.get("/teachers", response_model=List[Teacher])
def get_teachers():
    """Get all teachers"""
    return list(teachers_db.values())

@app.get("/teachers/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int):
    """Get a specific teacher by ID"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teachers_db[teacher_id]

@app.post("/teachers", response_model=Teacher, status_code=201)
def create_teacher(teacher: TeacherCreate):
    """Create a new teacher"""
    global teacher_id_counter
    new_teacher = Teacher(
        id=teacher_id_counter,
        name=teacher.name,
        subject=teacher.subject,
        email=teacher.email,
        years_of_experience=teacher.years_of_experience
    )
    teachers_db[teacher_id_counter] = new_teacher
    teacher_id_counter += 1
    return new_teacher

@app.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: int, teacher_update: TeacherUpdate):
    """Update an existing teacher"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    stored_teacher = teachers_db[teacher_id]
    update_data = teacher_update.model_dump(exclude_unset=True)
    
    updated_teacher = stored_teacher.model_copy(update=update_data)
    teachers_db[teacher_id] = updated_teacher
    return updated_teacher

@app.delete("/teachers/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: int):
    """Delete a teacher"""
    if teacher_id not in teachers_db:
        raise HTTPException(status_code=404, detail="Teacher not found")
    del teachers_db[teacher_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)