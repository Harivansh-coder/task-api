from fastapi import FastAPI
from .database import models
from .database.connection import engine
from .routers import auth, tasks, users
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to To-Do API, you can find the docs at /docs :)"}


# tasks routes
app.include_router(tasks.router)
# users routes
app.include_router(users.router)
# auth routes
app.include_router(auth.router)
