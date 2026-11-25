from pydantic import BaseModel, Field, AliasChoices
from typing import Optional, Dict, Any
from datetime import datetime

class SensorReadingCreate(BaseModel):
    deviceId: str = Field(default="plantiq-01", validation_alias=AliasChoices("deviceId", "device_id"))
    soilMoisture: Optional[float] = Field(None, validation_alias=AliasChoices("soilMoisture", "soil_moisture"))
    soilRaw: Optional[int] = Field(None, validation_alias=AliasChoices("soilRaw", "soil_raw"))
    temperature: Optional[float] = Field(None, validation_alias=AliasChoices("temperature", "temp"))
    humidity: Optional[float] = Field(None, validation_alias=AliasChoices("humidity"))
    distance: Optional[float] = Field(None, validation_alias=AliasChoices("distance"))
    personDetected: bool = Field(default=False, validation_alias=AliasChoices("personDetected", "person_detected"))
    timestamp: Optional[datetime] = None

    class Config:
        populate_by_name = True

class SensorReadingResponse(BaseModel):
    id: int
    deviceId: str = Field(..., validation_alias=AliasChoices("deviceId", "device_id"))
    soilMoisture: Optional[float] = Field(None, validation_alias=AliasChoices("soilMoisture", "soil_moisture"))
    soilRaw: Optional[int] = Field(None, validation_alias=AliasChoices("soilRaw", "soil_raw"))
    temperature: Optional[float] = Field(None, validation_alias=AliasChoices("temperature"))
    humidity: Optional[float] = Field(None, validation_alias=AliasChoices("humidity"))
    distance: Optional[float] = Field(None, validation_alias=AliasChoices("distance"))
    personDetected: bool = Field(False, validation_alias=AliasChoices("personDetected", "person_detected"))
    timestamp: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class EventCreate(BaseModel):
    deviceId: str = Field(default="plantiq-01", alias="deviceId")
    event: str = Field(..., alias="event") # "personDetected", "plantNeedsWater", etc.
    distance: Optional[float] = Field(None, alias="distance")
    timestamp: Optional[datetime] = None

    class Config:
        populate_by_name = True

class EventResponse(BaseModel):
    id: int
    deviceId: str
    event: str
    distance: Optional[float]
    greetingText: Optional[str]
    timestamp: datetime
    isRead: bool

    class Config:
        from_attributes = True

class PlantStatusResponse(BaseModel):
    statusCode: str # "HEALTHY", "NEEDS_WATER", "VERY_DRY", "TOO_WET", "HIGH_TEMPERATURE", "LOW_HUMIDITY", "SENSOR_ERROR"
    statusLabel: str # e.g. "Healthy 🟢", "Needs Water 💧"
    recommendation: str # e.g. "Your plant is healthy."
    contextualGreeting: str # e.g. "Hello! Welcome back! I'm feeling great today."
    sensorsWorking: Dict[str, bool] # {"soil": True, "dht22": True, "ultrasonic": True}
    deviceOnline: bool
    lastUpdated: Optional[datetime]
    currentReading: Optional[SensorReadingResponse]

class PlantProfileSchema(BaseModel):
    name: str = "Ferny"
    plantType: str = "Boston Fern"
    idealMoistureMin: float = 40.0
    idealMoistureMax: float = 75.0
    idealTempMin: float = 18.0
    idealTempMax: float = 28.0
    idealHumidityMin: float = 50.0
    idealHumidityMax: float = 80.0

    class Config:
        from_attributes = True

class PlantHistorySummary(BaseModel):
    timeframe: str
    avgMoisture: Optional[float]
    minMoisture: Optional[float]
    maxMoisture: Optional[float]
    avgTemp: Optional[float]
    minTemp: Optional[float]
    maxTemp: Optional[float]
    avgHumidity: Optional[float]
    minHumidity: Optional[float]
    maxHumidity: Optional[float]
    readings: list[SensorReadingResponse]
