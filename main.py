from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
# from database import engine, SessionLocal

app = FastAPI()

@app.get('/', status_code=status.HTTP_200_OK)
async def welcome():
    return {'welcome to student crud fast api appliaction'}