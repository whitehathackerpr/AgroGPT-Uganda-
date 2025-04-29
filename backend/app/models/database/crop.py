from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base

class CropDB(Base):
    __tablename__ = "crops"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    variety = Column(String, nullable=False)
    planting_date = Column(DateTime, nullable=False)
    expected_harvest_date = Column(DateTime, nullable=False)
    field_location = Column(String, nullable=False)
    area_size = Column(Float, nullable=False)  # in hectares
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with User model
    user = relationship("UserDB", back_populates="crops")

    def __repr__(self):
        return f"<Crop {self.name} ({self.variety})>" 