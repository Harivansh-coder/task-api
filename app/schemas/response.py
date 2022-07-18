from datetime import datetime
from app.schemas.user import UserOut
from .task import Task


class TaskResponse(Task):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(UserOut):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
