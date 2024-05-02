from fastapi import FastAPI, Response
from app.routers import mobile, slack
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(slack.router)
app.include_router(mobile.router)


@app.get("/")
async def root():
    return {"message": "Good morning!"}


@app.get("/cron")
async def cron():
    return {"message": "Good morning from cron!"}
