from fastapi import FastAPI
from app.routers import mobile, slack

app = FastAPI()

app.include_router(slack.router)
app.include_router(mobile.router)
