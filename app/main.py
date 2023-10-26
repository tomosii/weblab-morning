from fastapi import FastAPI
from app.routers import mobile, slack
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()


app.include_router(slack.router)
app.include_router(mobile.router)
