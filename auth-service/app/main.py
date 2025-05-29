from fastapi import FastAPI
from app.routers import auth, user_auth

app = FastAPI()

app.include_router(user_auth.router)
app.include_router(auth.router)
