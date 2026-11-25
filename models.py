from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from datetime import datetime
from backend.database import Base

class SensorReadingDB(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, default="plantiq-01")
    soil_moisture = Column(Float, nullable=True) # Percentage 0-100
    soil_raw = Column(Integer, nullable=True)     # Raw ADC value
    temperature = Column(Float, nullable=True)    # °C
    humidity = Column(Float, nullable=True)       # %
    distance = Column(Float, nullable=True)       # cm
    person_detected = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class PlantEventDB(Base):
    __tablename__ = "plant_events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True, default="plantiq-01")
    event_type = Column(String, index=True) # e.g. "personDetected", "plantNeedsWater", etc.
    distance = Column(Float, nullable=True)
    greeting_text = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    is_read = Column(Boolean, default=False)

class PlantProfileDB(Base):
    __tablename__ = "plant_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Ferny")
    plant_type = Column(String, default="Boston Fern")
    ideal_moisture_min = Column(Float, default=40.0)
    ideal_moisture_max = Column(Float, default=75.0)
    ideal_temp_min = Column(Float, default=18.0)
    ideal_temp_max = Column(Float, default=28.0)
    ideal_humidity_min = Column(Float, default=50.0)
    ideal_humidity_max = Column(Float, default=80.0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
