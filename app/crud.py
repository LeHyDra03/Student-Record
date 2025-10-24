from sqlmodel import Session, select
from app.models import Student
from app.database import engine
from typing import List, Optional


def create_student(student: Student) -> Student:
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


def get_students() -> List[Student]:
    with Session(engine) as session:
        statement = select(Student)
        results = session.exec(statement).all()
        return results


def get_student(student_id: int) -> Optional[Student]:
    with Session(engine) as session:
        student = session.get(Student, student_id)
        return student


def update_student(student_id: int, new_data: dict) -> Optional[Student]:
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
           return None
        for key, value in new_data.items():
           setattr(student, key, value)
        session.add(student)
        session.commit()
        session.refresh(student)
        return student


def delete_student(student_id: int) -> bool:
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            return False
        session.delete(student)
        session.commit()
        return True