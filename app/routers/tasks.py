from fastapi import APIRouter, status, UploadFile, File, BackgroundTasks, WebSocket
import pandas as pd
from app.definitions import TASK1_DIR, TASK2_DIR

router = APIRouter(
    tags=["data"],
    responses={
        404: {"description": "Not found"},
        400: {"description": "Invalid data"}
    }
)

@router.post("/tasks/uploaddata", status_code=status.HTTP_202_ACCEPTED)
async def upload_data(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):

    background_tasks.add_task(process_data, file)

    return {"message": "File {} upload successfully"}

@router.websocket("/tasks/{task_id}")
async def tasks_ws_endpoint(websocket: WebSocket, task_id: str):
    await websocket.accept()
    while True:
        try:
            task = {}
            match task_id:
                case '1':
                    task = pd.read_csv(TASK1_DIR).to_dict('split')
                case '2':
                    task = pd.read_csv(TASK2_DIR).to_dict('split')
            
            await websocket.send_json(data=task)
            break
        except FileNotFoundError as ex:
            continue

def process_data(file: UploadFile):
    df = pd.read_csv(file.file)
    selected = df.loc[:, ["education", "workclass", "hours-per-week"]]

    # calculate percentage of each education type
    processed_task1 = selected.education.value_counts(normalize=True).rename_axis('education').to_frame('percentage')
    
    # calculate average of hours-per-week for each workclass type
    processed_task2 = selected.groupby("workclass").apply(compute_mean)

    processed_task1.to_csv(TASK1_DIR)
    processed_task2.to_csv(TASK2_DIR)

def compute_mean(x):
    result = {"hpw_mean": x["hours-per-week"].mean()}
    return pd.Series(result, name="mean")
