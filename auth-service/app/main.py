from fastapi import FastAPI

app = FastAPI()


@app.get("/health-check/")
async def root() -> bool:
    return True
