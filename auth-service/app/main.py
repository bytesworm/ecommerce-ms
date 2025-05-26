from fastapi import FastAPI
from app.routers import user_auth

app = FastAPI()

app.include_router(user_auth.router)
