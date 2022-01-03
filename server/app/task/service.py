from app.settings import TASK1_TABLE, TASK2_TABLE
import pandas as pd
from pandas.errors import ParserError
from fastapi import UploadFile, BackgroundTasks
from app.utils.app_exceptions import AppException


class TaskService:
    async def handle_data_upload(self, file: UploadFile, background_tasks: BackgroundTasks):
        message = ""
        try:
            df = pd.read_csv(file.file)

            background_tasks.add_task(self.__process_data, df)
        except ParserError as e:
            message = f"Invalid file {file.filename}, {e}"
            raise AppException(message)
        else:
            message = f"File {file.filename} upload successfully"

        return message

    def __process_data(self, df: pd.DataFrame):
        selected = df.loc[:, ["education", "workclass", "hours-per-week"]]

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

    async def retrieve_data(self, task_id: str):
        task = {}
        match task_id:
            case '1':
                task = pd.read_csv(TASK1_TABLE).to_dict('split')
            case '2':
                task = pd.read_csv(TASK2_TABLE).to_dict('split')

        return task