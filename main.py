from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from fastapi.staticfiles import StaticFiles
from routers.default_router import default_router
from routers.workout_router import workout_router

from db_conn import connect_to_mongodb, get_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Startup: Connect to MongoDB
        app.mongodb_client = await connect_to_mongodb()
        app.mongodb = get_database(app.mongodb_client)
        print("Connected to MongoDB")

        yield
    except:
        print("Unable to connect to MongoDB")
    finally:
        app.mongodb_client.close()
        print("Disconnected from MongoDB")

app = FastAPI(
    title="MongoDB Tutorial for Dummies",
    description="Learning MongoDB with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    handlers=[
        logging.StreamHandler(), 
    ]
)
logger = logging.getLogger(__name__) 


app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(default_router)
app.include_router(workout_router, prefix="/workouts", tags=["workouts"])
