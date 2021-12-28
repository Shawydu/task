from fastapi import FastAPI
from app.database import db_helper

from app.routers import tasks

app = FastAPI()


app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome!"}
