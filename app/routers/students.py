from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/students", tags=["students"])

# Pydantic models
class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    email: Optional[str] = Field(None, max_length=200)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    email: Optional[str] = Field(None, max_length=200)

class Student(StudentBase):
    id: int

# In-memory storage (簡易示範用，實務應改為資料庫)
_students: Dict[int, Student] = {}
_next_id: int = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

@router.get("/", response_model=List[Student])
async def list_students() -> List[Student]:
    return list(_students.values())

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int) -> Student:
    student = _students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(payload: StudentCreate) -> Student:
    sid = _get_next_id()
    student = Student(id=sid, **payload.model_dump())
    _students[sid] = student
    return student

@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, payload: StudentUpdate) -> Student:
    existing = _students.get(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")
    update_data = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=update_data)
    _students[student_id] = updated
    return updated

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int) -> None:
    if student_id not in _students:
        raise HTTPException(status_code=404, detail="Student not found")
    del _students[student_id]
    return None
