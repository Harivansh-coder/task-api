from fastapi import FastAPI
from .database import models
from .database.connection import engine
from .routers import tasks, users

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


app.include_router(tasks.router)
app.include_router(users.router)
