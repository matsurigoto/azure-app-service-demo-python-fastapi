from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/employees", tags=["employees"])

# Pydantic models
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=200)
    salary: Optional[float] = Field(None, ge=0)

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=200)
    salary: Optional[float] = Field(None, ge=0)

class Employee(EmployeeBase):
    id: int

# In-memory storage (示範用途，正式環境應使用資料庫)
_employees: Dict[int, Employee] = {}
_next_id: int = 1

def _get_next_id() -> int:
    global _next_id
    nid = _next_id
    _next_id += 1
    return nid

@router.get("/", response_model=List[Employee])
async def list_employees() -> List[Employee]:
    return list(_employees.values())

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int) -> Employee:
    employee = _employees.get(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(payload: EmployeeCreate) -> Employee:
    eid = _get_next_id()
    employee = Employee(id=eid, **payload.model_dump())
    _employees[eid] = employee
    return employee

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, payload: EmployeeUpdate) -> Employee:
    existing = _employees.get(employee_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Employee not found")
    update_data = payload.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=update_data)
    _employees[employee_id] = updated
    return updated

@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int) -> None:
    if employee_id not in _employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    del _employees[employee_id]
    return None