from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.database import engine, Base
from backend.routes import sensor, events, health
from backend.config import settings

# Create database tables on application start
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="PlantIQ - Smart Talking Plant Ecosystem API",
    version="1.0.0"
)

# Enable CORS for cross-origin requests from iOS app / Web Simulator
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(sensor.router)
app.include_router(events.router)
app.include_router(health.router)

# Mount web simulator static files if directory exists
simulator_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web_simulator")
if os.path.exists(simulator_dir):
    app.mount("/simulator", StaticFiles(directory=simulator_dir, html=True), name="simulator")

@app.get("/")
def root():
    return {
        "project": "PlantIQ API",
        "tagline": "Your plant. Smarter. 🌱",
        "docs": "/docs",
        "health": "/api/health",
        "simulator": "/simulator"
    }
