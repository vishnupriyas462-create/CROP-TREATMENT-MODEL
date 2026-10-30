import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    PROJECT_NAME: str = "AgriGuard AI — Smart Crop Health Assistant"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    CORS_ORIGINS: list[str] = [
        origin.strip() 
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173").split(",")
        if origin.strip()
    ]
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'agri_guard.db'}")
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "ml_weights" / "mobilenetv2_plantvillage.pth"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.60"))
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")
    
    ENABLE_IMAGE_STORAGE: bool = os.getenv("ENABLE_IMAGE_STORAGE", "true").lower() in ("true", "1", "yes")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))
    MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
    
    ALLOWED_IMAGE_EXTENSIONS: set[str] = {"jpg", "jpeg", "png", "webp"}
    ALLOWED_MIME_TYPES: set[str] = {"image/jpeg", "image/png", "image/webp"}

settings = Settings()
