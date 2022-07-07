from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    email: str
    password: str


class Task(BaseModel):
    title: str
    description: str
    completed: bool = False


my_tasks = []


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


@app.get("/tasks")
def get_tasks():
    return{"tasks": my_tasks, "count": len(my_tasks)}


@app.post("/tasks/create")
def create_task(task: Task):
    temp = task.dict()
    temp["id"] = range(5)
    my_tasks.append(temp)
    return {"task": task}


@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    for i in my_tasks:
        if task_id == i["id"]:
            return {"task_id": i}


@app.patch("tasks")
def update_task(task: Task):
    return {"message": "done"}
