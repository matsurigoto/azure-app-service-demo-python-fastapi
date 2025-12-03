from typing import Union, Optional, List
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Student data model
class StudentBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    grade: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int


# Thread-safe in-memory storage for students (for demo purposes)
# Note: In production, use a proper database
students_db: dict[int, Student] = {}
student_id_counter: int = 1
students_lock = threading.Lock()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/status")
def read_status():
    return {"Status": "Success"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Student API endpoints
@app.get("/students", response_model=List[Student])
def get_students():
    """Get all students"""
    with students_lock:
        return list(students_db.values())


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    """Get a student by ID"""
    with students_lock:
        if student_id not in students_db:
            raise HTTPException(status_code=404, detail="Student not found")
        return students_db[student_id]


@app.post("/students", response_model=Student, status_code=201)
def create_student(student: StudentCreate):
    """Create a new student"""
    global student_id_counter
    with students_lock:
        new_student = Student(id=student_id_counter, **student.model_dump())
        students_db[student_id_counter] = new_student
        student_id_counter += 1
        return new_student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate):
    """Update a student by ID"""
    with students_lock:
        if student_id not in students_db:
            raise HTTPException(status_code=404, detail="Student not found")
        updated_student = Student(id=student_id, **student.model_dump())
        students_db[student_id] = updated_student
        return updated_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    """Delete a student by ID"""
    with students_lock:
        if student_id not in students_db:
            raise HTTPException(status_code=404, detail="Student not found")
        del students_db[student_id]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)