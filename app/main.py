from typing import Union, Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic models for Student
class StudentBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    major: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    major: Optional[str] = None

class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

# In-memory storage for students
students_db: dict[int, Student] = {}
next_id = 1

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status}")
def read_root():
    return {"Status": "Success"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Student CRUD endpoints
@app.post("/students", response_model=Student, status_code=201)
async def create_student(student: StudentCreate):
    """Create a new student"""
    global next_id
    new_student = Student(id=next_id, **student.model_dump())
    students_db[next_id] = new_student
    next_id += 1
    return new_student

@app.get("/students", response_model=List[Student])
async def get_students():
    """Get all students"""
    return list(students_db.values())

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """Get a specific student by ID"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student_update: StudentUpdate):
    """Update a student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    stored_student = students_db[student_id]
    update_data = student_update.model_dump(exclude_unset=True)
    
    updated_student = stored_student.model_copy(update=update_data)
    students_db[student_id] = updated_student
    return updated_student

@app.delete("/students/{student_id}", status_code=204)
async def delete_student(student_id: int):
    """Delete a student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)