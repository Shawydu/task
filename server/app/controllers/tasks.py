from fastapi import APIRouter, status, UploadFile, File, BackgroundTasks, WebSocket, HTTPException
from app.apis.api_task import handle_data_upload
import pandas as pd
from pandas.errors import ParserError
from app.definitions import TASK1_DIR, TASK2_DIR

router = APIRouter(
    tags=["task"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid data"}
    }
)

@router.post("/tasks/uploaddata", status_code=status.HTTP_202_ACCEPTED)
async def upload_data(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    print(file.filename)
    handle_data_upload(file, background_tasks)

@router.websocket("/tasks/{task_id}")
async def tasks_ws_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    while True:
        try:
            task = await retrieve_data(task_id)
            await websocket.send_json(data=task)
            break
        except FileNotFoundError as ex:
            continue

async def retrieve_data(task_id: str):
    task = {}
    match task_id:
        case '1':
            task = pd.read_csv(TASK1_DIR).to_dict('split')
        case '2':
            task = pd.read_csv(TASK2_DIR).to_dict('split')

    return task
