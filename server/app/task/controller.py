from fastapi import APIRouter, status, UploadFile, File, WebSocket, BackgroundTasks
from fastapi.exceptions import HTTPException
from .service import TaskService
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
        result = await TaskService().handle_data_upload(file, background_tasks)
    except AppException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    return result

@router.websocket(
    "/{task_id}"
)
async def tasks_ws_endpoint(websocket: WebSocket, task_id: str):
    """
    open websocket session retrieve calculated data
    """
    await websocket.accept()
    while True:
        try:
            task = await TaskService().retrieve_data(task_id)
            await websocket.send_json(data=task)
            break
        except FileNotFoundError:
            continue

