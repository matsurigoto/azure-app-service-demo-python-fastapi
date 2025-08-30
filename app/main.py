from typing import Union, Optional, List, Dict
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Azure App Service Demo - FastAPI")


# =====================
# Models
# =====================
class InstructorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="講師姓名")
    expertise: Optional[str] = Field(None, max_length=200, description="專長領域")


class InstructorCreate(InstructorBase):
    pass


class InstructorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    expertise: Optional[str] = Field(None, max_length=200)


class Instructor(InstructorBase):
    id: int


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="學生姓名")
    student_id: Optional[str] = Field(None, max_length=20, description="學號")
    email: Optional[str] = Field(None, max_length=100, description="電子郵件")
    major: Optional[str] = Field(None, max_length=100, description="主修科系")
    year: Optional[int] = Field(None, ge=1, le=7, description="年級")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    student_id: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    major: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=7)


class Student(StudentBase):
    id: int


# =====================
# In-memory storage
# =====================
_instructors: Dict[int, Instructor] = {}
_next_instructor_id: int = 1

_students: Dict[int, Student] = {}
_next_student_id: int = 1


def _get_next_instructor_id() -> int:
    global _next_instructor_id
    nid = _next_instructor_id
    _next_instructor_id += 1
    return nid


def _get_next_student_id() -> int:
    global _next_student_id
    nid = _next_student_id
    _next_student_id += 1
    return nid

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/status", summary="服務健康檢查")
def read_status():
    return {"status": "ok"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# =====================
# Instructor CRUD Routes
# =====================

@app.post("/instructors", response_model=Instructor, status_code=status.HTTP_201_CREATED, summary="新增講師")
def create_instructor(payload: InstructorCreate):
    new_id = _get_next_instructor_id()
    instructor = Instructor(id=new_id, **payload.model_dump())
    _instructors[new_id] = instructor
    return instructor


@app.get("/instructors", response_model=List[Instructor], summary="取得全部講師")
def list_instructors():
    return list(_instructors.values())


@app.get("/instructors/{instructor_id}", response_model=Instructor, summary="取得單一講師")
def get_instructor(instructor_id: int):
    instructor = _instructors.get(instructor_id)
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return instructor


@app.put("/instructors/{instructor_id}", response_model=Instructor, summary="完整更新講師")
def replace_instructor(instructor_id: int, payload: InstructorCreate):
    if instructor_id not in _instructors:
        raise HTTPException(status_code=404, detail="Instructor not found")
    updated = Instructor(id=instructor_id, **payload.model_dump())
    _instructors[instructor_id] = updated
    return updated


@app.patch("/instructors/{instructor_id}", response_model=Instructor, summary="部分更新講師")
def update_instructor(instructor_id: int, payload: InstructorUpdate):
    existing = _instructors.get(instructor_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Instructor not found")
    data = existing.model_dump()
    update_data = payload.model_dump(exclude_unset=True)
    data.update({k: v for k, v in update_data.items() if v is not None})
    updated = Instructor(**data)
    _instructors[instructor_id] = updated
    return updated


@app.delete("/instructors/{instructor_id}", status_code=status.HTTP_204_NO_CONTENT, summary="刪除講師")
def delete_instructor(instructor_id: int):
    if instructor_id not in _instructors:
        raise HTTPException(status_code=404, detail="Instructor not found")
    del _instructors[instructor_id]
    return None


# =====================
# Student CRUD Routes
# =====================

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED, summary="新增學生")
def create_student(payload: StudentCreate):
    new_id = _get_next_student_id()
    student = Student(id=new_id, **payload.model_dump())
    _students[new_id] = student
    return student


@app.get("/students", response_model=List[Student], summary="取得全部學生")
def list_students():
    return list(_students.values())


@app.get("/students/{student_id}", response_model=Student, summary="取得單一學生")
def get_student(student_id: int):
    student = _students.get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=Student, summary="完整更新學生")
def replace_student(student_id: int, payload: StudentCreate):
    if student_id not in _students:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = Student(id=student_id, **payload.model_dump())
    _students[student_id] = updated
    return updated


@app.patch("/students/{student_id}", response_model=Student, summary="部分更新學生")
def update_student(student_id: int, payload: StudentUpdate):
    existing = _students.get(student_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")
    data = existing.model_dump()
    update_data = payload.model_dump(exclude_unset=True)
    data.update({k: v for k, v in update_data.items() if v is not None})
    updated = Student(**data)
    _students[student_id] = updated
    return updated


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="刪除學生")
def delete_student(student_id: int):
    if student_id not in _students:
        raise HTTPException(status_code=404, detail="Student not found")
    del _students[student_id]
    return None