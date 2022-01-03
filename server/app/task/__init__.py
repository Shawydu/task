from fastapi import FastAPI

BASE_ROUTE = "task"

def register_routes(app: FastAPI, root="api/v1"):
    from .controller import router as task_router

    app.include_router(task_router, prefix=f"/{root}/{BASE_ROUTE}")