import asyncio
import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

app = FastAPI()

db_ready = False

async def initialize_database():    
    global db_ready
    logger.info("Starting database initialization...")
    await asyncio.sleep(20)  # Simulate a time-consuming initialization task
    db_ready = True
    logger.info("Database initialization completed.")

@app.lifespan
async def lifespan(app: FastAPI):
    # Startup
    asyncio.create_task(initialize_database())
    yield
    # Shutdown (if needed)

@app.get("/")
async def root():
    logger.info("Calling Root endpoint.")
    return {"message": "Hello backend service!"}

@app.get("/health")
async def service_health_check():
    logger.info("Calling /health check endpoint.")
    return {"status": "healthy"}, 200

@app.get("/db-health")
async def db_health_check():
    logger.info("Calling /db-health check endpoint.")
    if db_ready:
        logger.info("Database is ready.")
        return {"status": "Ok"}, 200
    logger.info("Database is not ready.")
    return {"status": "starting..."}, 503