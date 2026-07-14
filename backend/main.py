import logging

from fastapi import FastAPI
from routes.mentor_routes import router as mentor_router
from backend.config import APP_NAME, DEBUG
from database.connection import Base, engine
import models.db_models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, debug=DEBUG)

app.include_router(mentor_router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": f"{APP_NAME} is running",
        "data": {}
    }
