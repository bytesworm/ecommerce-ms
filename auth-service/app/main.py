from fastapi import FastAPI
from app.routers import auth, health, user_auth

app = FastAPI(root_path="/auth")

app.include_router(user_auth.router)
app.include_router(auth.router)
app.include_router(health.router)
