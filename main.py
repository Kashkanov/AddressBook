import logging
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import adressess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s" 
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
logger.info("Database created!")

app = FastAPI()

app.include_router(adressess.router)

@app.get("/", tags=["Health"])
async def root() -> dict:
    return {"status": "ok"}
