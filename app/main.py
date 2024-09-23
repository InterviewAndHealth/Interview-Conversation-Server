from fastapi import FastAPI

from app.routers import interviews

app = FastAPI()

app.include_router(interviews.router)


@app.get("/")
async def root():
    return {"message": "Interviews Conversation API"}
