import pandas as pd
from app.settings import TASK1_TABLE, TASK2_TABLE
from pandas.errors import ParserError
from fastapi import UploadFile, BackgroundTasks
from app.utils.app_exceptions import AppException
from .schema import TaskSchema

expected_columns = ["education", "workclass", "hours-per-week"]

class TaskService:
    def handle_data_upload(self, file: UploadFile, background_tasks: BackgroundTasks):
        message = ""
        try:
            df = pd.read_csv(file.file)
            if not set(expected_columns).issubset(df.columns):
                raise AppException(f"expected columns not found: {expected_columns}")
            # add data processing task to the background tasks list, so that processing handled asynchronously 
            background_tasks.add_task(self.__process_data, df)
        except (ParserError, AppException) as e:
        # defer validation message to controller, by raising a custom exception
            message = f"Invalid file {file.filename}, {e}"
            raise AppException(message)
        else:
            message = f"File {file.filename} upload successfully"

        return message

    def __process_data(self, df: pd.DataFrame):
        selected = df.loc[:, expected_columns]

        # calculate percentage of each education type
        processed_task1 = selected.education.value_counts(normalize=True).rename_axis('education').to_frame('percentage')
        
        # calculate average of hours-per-week for each workclass type
        processed_task2 = selected.groupby("workclass").apply(self.compute_mean)

        processed_task1.to_csv(TASK1_TABLE)
        processed_task2.to_csv(TASK2_TABLE)

    @staticmethod
    def compute_mean(x):
        result = {"hours-per-week average": x["hours-per-week"].mean()}
        return pd.Series(result, name="mean")

    def retrieve_data(self, task_id: str) -> TaskSchema:
        task = {}
        try:
            # ideally task_id is unique, which indexes calculation results for both "education distribution" and "hours-per-week average"
            match task_id:
                case '1':
                    task = pd.read_csv(TASK1_TABLE).to_dict('split')
                case '2':
                    task = pd.read_csv(TASK2_TABLE).to_dict('split')
        except FileNotFoundError:
            raise AppException("data not found")

        if len(task) == 0:
            raise AppException("data not found")
            
        return TaskSchema(**task)
