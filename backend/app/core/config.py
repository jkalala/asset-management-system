from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Asset Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_ToCA6Ux2GyMa@ep-jolly-glade-a8xgwksm-pooler.eastus2.azure.neon.tech/neondb?sslmode=require")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "V7S0n9RkiiI3Zbme7z_Nt4GX2f8QaTThf9QEYZmkk2k")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

# Create the database directory if it doesn't exist
os.makedirs(os.path.dirname(Settings().DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

settings = Settings() 