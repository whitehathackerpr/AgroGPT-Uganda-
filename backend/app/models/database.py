from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

Base = declarative_base()

class UserType(enum.Enum):
    FARMER = "farmer"
    EXTENSION_OFFICER = "extension_officer"
    RESEARCHER = "researcher"
    POLICYMAKER = "policymaker"

class Language(enum.Enum):
    ENGLISH = "en"
    LUGANDA = "lg"
    RUNYANKOLE = "nyn"
    ACHOLI = "ach"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type = Column(Enum(UserType))
    language = Column(Enum(Language))
    region = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Crop(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    scientific_name = Column(String)
    description = Column(String)
    optimal_conditions = Column(String)
    common_diseases = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Disease(Base):
    __tablename__ = "diseases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    description = Column(String)
    symptoms = Column(String)
    treatment = Column(String)
    prevention = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    crop = relationship("Crop")

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    region = Column(String)
    price = Column(Float)
    unit = Column(String)
    date = Column(DateTime)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    crop = relationship("Crop")

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    rainfall = Column(Float)
    wind_speed = Column(Float)
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class PlantingCalendar(Base):
    __tablename__ = "planting_calendars"

    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    region = Column(String)
    planting_start = Column(DateTime)
    planting_end = Column(DateTime)
    harvesting_start = Column(DateTime)
    harvesting_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    crop = relationship("Crop") 