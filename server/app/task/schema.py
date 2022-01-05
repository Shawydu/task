from typing import List
from app.base import BaseModel

class TaskSchema(BaseModel):
    index: List
    columns: List
    data: List
