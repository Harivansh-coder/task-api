from random import randint
from fastapi import FastAPI, HTTPException, status
import psycopg2
from psycopg2.extras import RealDictCursor
from app.models.task import Task

app = FastAPI()


my_tasks = []

try:
    con = psycopg2.connect(host='localhost', database='task-api-db',
                           user='postgres', password='1234', cursor_factory=RealDictCursor)

    cursor = con.cursor()
    print("connection successful")

except Exception as error:
    print(error)


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


@app.get("/tasks")
def get_tasks():
    cursor.execute("""SELECT * FROM tasks""")
    tasks = cursor.fetchall()
    return{"tasks": tasks, "count": len(tasks)}


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
