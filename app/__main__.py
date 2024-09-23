import uvicorn

from app import PORT
from app.main import app

uvicorn.run(app, host="localhost", port=PORT)
