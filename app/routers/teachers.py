from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/teachers", tags=["teachers"])

# Pydantic models
class TeacherBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    subject: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=200)

class TeacherCreate(TeacherBase):
    pass

class TeacherUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=200)

class Teacher(TeacherBase):
    id: int

# In-memory storage (示範用途，正式環境應使用資料庫)
_teachers: Dict[int, Teacher] = {}
_next_id: int = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

@router.get("/", response_model=List[Teacher])
async def list_teachers() -> List[Teacher]:
    return list(_teachers.values())

@router.get("/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: int) -> Teacher:
    teacher = _teachers.get(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.post("/", response_model=Teacher, status_code=status.HTTP_201_CREATED)
async def create_teacher(payload: TeacherCreate) -> Teacher:
    tid = _get_next_id()
    teacher = Teacher(id=tid, **payload.model_dump())
    _teachers[tid] = teacher
    return teacher

@router.put("/{teacher_id}", response_model=Teacher)
async def update_teacher(teacher_id: int, payload: TeacherUpdate) -> Teacher:
    existing = _teachers.get(teacher_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Teacher not found")
    update_data = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=update_data)
    _teachers[teacher_id] = updated
    return updated

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id: int) -> None:
    if teacher_id not in _teachers:
        raise HTTPException(status_code=404, detail="Teacher not found")
    del _teachers[teacher_id]
    return None
