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
    cursor.execute("""INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING *""",
                   (task.title, task.description))
    new_task = cursor.fetchone()
    con.commit()
    return {"task": new_task}


@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    cursor.execute("""SELECT * FROM tasks WHERE id = %s """, (str(task_id)))
    task = cursor.fetchone()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id {task_id} not found")

    return {"task_id": task}


@app.patch("/tasks")
def update_task(task: Task):
    return {"message": "done"}


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTask():
    pass
