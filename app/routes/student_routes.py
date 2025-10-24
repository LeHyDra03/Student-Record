from fastapi import APIRouter, HTTPException
from app.schemas import StudentCreate, StudentUpdate
from app.models import Student
import app.crud as crud


router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=Student)
def create_student_endpoint(student: StudentCreate):
    # convert schema to model
    student_obj = Student.from_orm(student)
    created = crud.create_student(student_obj)
    return created


@router.get("/", response_model=list[Student])
def read_students():
    return crud.get_students()


@router.get("/{student_id}", response_model=Student)
def read_student(student_id: int):
    student = crud.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=Student)
def update_student_endpoint(student_id: int, payload: StudentUpdate):
    data = payload.dict(exclude_unset=True)
    updated = crud.update_student(student_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@router.delete("/{student_id}")
def delete_student_endpoint(student_id: int):
    ok = crud.delete_student(student_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}