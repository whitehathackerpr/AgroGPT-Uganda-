from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .user import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    location = Column(String)
    size_hectares = Column(Float)
    main_crops = Column(String)  # Comma-separated list of crops
    soil_type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Relationships
    owner = relationship("User", back_populates="farms") 