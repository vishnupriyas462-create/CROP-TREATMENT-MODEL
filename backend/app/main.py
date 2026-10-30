"""
AgriGuard AI — Smart Crop Health Assistant
FastAPI Application Entry Point.
"""

from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.data.seed_data import seed_database
from app.ml.inference import CropDiseaseClassifier
from app.routers import (
    health,
    crops,
    predict,
    history,
    recommendations,
    feedback,
    analytics
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("agriguard.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize SQLite Database & Tables
    logger.info("Initializing database tables...")
    init_db()

    # 2. Seed verified knowledge base and crops
    logger.info("Seeding verified agricultural guidance...")
    seed_database()

    # 3. Preload PyTorch Model
    logger.info("Initializing PyTorch MobileNetV2 classifier...")
    classifier = CropDiseaseClassifier.get_instance()
    logger.info(f"Model initialized. Weights loaded: {classifier.model_loaded}")

    # 4. Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    yield

    logger.info("Shutting down AgriGuard AI backend service.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Farmer-friendly AI platform for plant disease detection, verified pesticide recommendations, and integrated pest management.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if "*" not in settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api
app.include_router(health.router, prefix="/api")
app.include_router(crops.router, prefix="/api")
app.include_router(predict.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs_url": "/docs",
        "health_check": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
