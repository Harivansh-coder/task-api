from random import randint
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from app.models.task import Task

app = FastAPI()


my_tasks = []


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


@app.get("/tasks")
def get_tasks():
    return{"tasks": my_tasks, "count": len(my_tasks)}


@app.post("/tasks/create", status_code=status.HTTP_201_CREATED)
def create_task(task: Task):
    temp = task.dict()
    temp["id"] = randint(0, 1000000)
    my_tasks.append(temp)
    return {"task": my_tasks}


@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    for i in my_tasks:
        if task_id == i["id"]:
            return {"task_id": i}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"task with id {task_id} not found")


@app.patch("/tasks")
def update_task(task: Task):
    return {"message": "done"}


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTask():
    pass
