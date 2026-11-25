from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PlantIQ API"
    DATABASE_URL: str = "sqlite:///./plantiq.db"
    
    # Configurable sensor thresholds
    SOIL_VERY_DRY_MAX: float = 25.0
    SOIL_NEEDS_WATER_MAX: float = 40.0
    SOIL_HEALTHY_MAX: float = 75.0
    
    TEMP_HIGH_THRESHOLD: float = 30.0
    TEMP_LOW_THRESHOLD: float = 10.0
    
    HUMIDITY_LOW_THRESHOLD: float = 40.0
    HUMIDITY_HIGH_THRESHOLD: float = 85.0
    
    # Presence detection settings
    PRESENCE_COOLDOWN_SECONDS: int = 15
    DEVICE_OFFLINE_TIMEOUT_SECONDS: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
