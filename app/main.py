from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

# Student models
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Student's full name")
    email: EmailStr = Field(..., description="Student's email address")
    age: int = Field(..., ge=16, le=100, description="Student's age (16-100)")
    major: Optional[str] = Field(None, max_length=100, description="Student's major/field of study")

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Student's full name")
    email: Optional[EmailStr] = Field(None, description="Student's email address")
    age: Optional[int] = Field(None, ge=16, le=100, description="Student's age (16-100)")
    major: Optional[str] = Field(None, max_length=100, description="Student's major/field of study")

class Student(StudentBase):
    id: int = Field(..., description="Unique student identifier")

# In-memory storage
students_db: List[Student] = []
next_student_id = 1

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

# Student CRUD endpoints

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    """Create a new student."""
    global next_student_id
    
    # Check if email already exists
    for existing_student in students_db:
        if existing_student.email == student.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this email already exists"
            )
    
    new_student = Student(
        id=next_student_id,
        **student.model_dump()
    )
    students_db.append(new_student)
    next_student_id += 1
    
    return new_student

@app.get("/students", response_model=List[Student])
async def get_students():
    """Get all students."""
    return students_db

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """Get a specific student by ID."""
    for student in students_db:
        if student.id == student_id:
            return student
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with id {student_id} not found"
    )

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, student_update: StudentUpdate):
    """Update a specific student by ID."""
    for i, student in enumerate(students_db):
        if student.id == student_id:
            # Check if email is being updated and if it conflicts with existing emails
            if student_update.email and student_update.email != student.email:
                for other_student in students_db:
                    if other_student.id != student_id and other_student.email == student_update.email:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Student with this email already exists"
                        )
            
            # Update only provided fields
            update_data = student_update.model_dump(exclude_unset=True)
            updated_student = student.model_copy(update=update_data)
            students_db[i] = updated_student
            return updated_student
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with id {student_id} not found"
    )

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    """Delete a specific student by ID."""
    for i, student in enumerate(students_db):
        if student.id == student_id:
            students_db.pop(i)
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with id {student_id} not found"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)