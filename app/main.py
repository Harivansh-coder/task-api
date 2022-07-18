from fastapi import FastAPI
from .database import models
from .database.connection import engine
from .routers import tasks, users, authentication

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


# tasks routes
app.include_router(tasks.router)
# users routes
app.include_router(users.router)
# auth routes
app.include_router(authentication.router)
