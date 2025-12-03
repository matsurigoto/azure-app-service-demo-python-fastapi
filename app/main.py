from typing import Union, Optional, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Student Pydantic models
class StudentBase(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    grade: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None


class Student(StudentBase):
    id: int


# In-memory storage for students
students_db: dict[int, dict[str, Any]] = {}
student_id_counter: int = 1


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
def create_student(student: StudentCreate):
    """Create a new student"""
    global student_id_counter
    student_id = student_id_counter
    student_id_counter += 1
    student_data = student.model_dump()
    student_data["id"] = student_id
    students_db[student_id] = student_data
    return student_data


@app.get("/students", response_model=list[Student])
def read_students():
    """Get all students"""
    return list(students_db.values())


@app.get("/students/{student_id}", response_model=Student)
def read_student(student_id: int):
    """Get a specific student by ID"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentUpdate):
    """Update a student by ID"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    existing_student = students_db[student_id]
    update_data = student.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        existing_student[key] = value
    students_db[student_id] = existing_student
    return existing_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    """Delete a student by ID"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    del students_db[student_id]
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)