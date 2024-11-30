from fastapi import FastAPI
from app.routers import users, utility
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(utility.router, prefix="/utility", tags=["Utility"])
