from fastapi import FastAPI, HTTPException, status, Response, Depends
from app.schemas.task import Task
from app.schemas.response import TaskResponse
from .database import models
from sqlalchemy.orm import Session
from .database.connection import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


@app.get("/tasks",  response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


@app.post("/tasks/create", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: Task, db: Session = Depends(get_db)):
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks/{task_id}",  response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id {task_id} not found")

    return task


@app.put("/tasks/{id}", response_model=TaskResponse)
def update_task(id: int, task: Task,  db: Session = Depends(get_db)):

    update_query = db.query(models.Task).filter(models.Task.id == id)

    # if task does not exits
    if not update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id {id} not found")
    # if task do exits
    update_query.update(task.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()


@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteTask(id: int,  db: Session = Depends(get_db)):

    deleted_task = db.query(models.Task).filter(models.Task.id == id)
    if not deleted_task.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"task with id {id} not found")
    deleted_task.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
