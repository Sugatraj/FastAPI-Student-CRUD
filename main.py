from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class StudentBase(BaseModel):
    name : str

class UpdateStudentBase(BaseModel):
    name: str

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get('/', status_code=status.HTTP_200_OK)
async def welcome():
    return {'welcome to student crud fast api appliaction'}

@app.post('/student', status_code=status.HTTP_201_CREATED)
async def create_student(student:StudentBase, db:db_dependency):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    return {'message' : "studnet created successfully"}

@app.get('/students/{id}', status_code=status.HTTP_200_OK)
async def read_students(id: int, db: db_dependency):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail='student not found')
    return student

@app.patch('/students/{id}', status_code=status.HTTP_200_OK)
async def update_student(id: int, student_update: UpdateStudentBase, db: db_dependency):
    db_student = db.query(models.Student).filter(models.Student.id == id).first()

    if db_student is None :
        raise HTTPException(status_code=404, detail='student not found')
    
    update_data = student_update.dict