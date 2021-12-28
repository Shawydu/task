from fastapi import APIRouter, status, UploadFile, File, BackgroundTasks
from fastapi.param_functions import Header
import pandas as pd
import json
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
# def upload_data(file: UploadFile):

    background_tasks.add_task(process_data, file)
    # process_data(file)
    print("I'm going first")
    return {"message": "File {} upload successfully".format(file.name)}

@router.get("/tasks/status", status_code=status.HTTP_200_OK)
def check_status():
    task1 = pd.read_csv(TASK1_DIR).to_dict('records')
    task2 = pd.read_csv(TASK2_DIR).to_dict('records')
    return {'task1': task1, 'task2': task2}

def process_data(file: UploadFile):
    df = pd.read_csv(file.file)
    selected = df.loc[:, ["education", "workclass", "hours-per-week"]]

    # calculate percentage of each education type
    processed_task1 = selected.education.value_counts(normalize=True).rename_axis('education').to_frame('percentage')
    
    # calculate average of hours-per-week for each workclass type
    processed_task2 = selected.groupby("workclass").apply(compute_mean)

    processed_task1.to_csv(TASK1_DIR)
    processed_task2.to_csv(TASK2_DIR)
    print("I'm going second")

def compute_mean(x):
    result = {"hpw_mean": x["hours-per-week"].mean()}
    return pd.Series(result, name="mean")
