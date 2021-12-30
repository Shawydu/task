from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import tasks

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome!"}
