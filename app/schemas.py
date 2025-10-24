from sqlmodel import SQLModel
from typing import Optional


class StudentCreate(SQLModel):
    name: str
    age: int
    grade: str
    email: str


class StudentRead(StudentCreate):
    id: int


class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    email: Optional[str] = None