from datetime import datetime
from .task import Task


class TaskResponse(Task):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
