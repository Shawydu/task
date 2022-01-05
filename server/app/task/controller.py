from fastapi import APIRouter, status, UploadFile, File, WebSocket, BackgroundTasks
from starlette.responses import JSONResponse
from .service import TaskService
from .schema import TaskSchema
from app.utils.app_exceptions import AppException

router = APIRouter(
    tags=["task"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid data"}
    }
)

@router.post(
    "/uploaddata", status_code=status.HTTP_202_ACCEPTED
)
async def upload_data(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """
    import data and defer calculation asynchronously
    """
    try:
        result = TaskService().handle_data_upload(file, background_tasks)
    except AppException as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": e.message})
    return {"message": result}

@router.websocket(
    "/{task_id}",
)
async def get_task(websocket: WebSocket, task_id: str) -> TaskSchema:
    """
    open websocket session retrieve calculated data
    """
    await websocket.accept()
    while True:
        try:
            await websocket.receive_text()
            task = TaskService().retrieve_data(task_id)
            await websocket.send_json(data=task.dict())
        except AppException as e:
            await websocket.send_json(data={"message": e.message})
            continue
