from fastapi import FastAPI
from app.routers import slack, user

app = FastAPI()

app.include_router(slack.router)
app.include_router(user.router)
