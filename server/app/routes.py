from fastapi import FastAPI

def register_routes(app: FastAPI):
    from app.task import register_routes as attach_task

    attach_task(app)
