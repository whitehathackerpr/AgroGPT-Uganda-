from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CropBase(BaseModel):
    name: str = Field(..., description="Name of the crop")
    variety: str = Field(..., description="Variety or cultivar of the crop")
    planting_date: datetime = Field(..., description="Date when the crop was planted")
    expected_harvest_date: datetime = Field(..., description="Expected harvest date")
    field_location: str = Field(..., description="Location of the field where crop is planted")
    area_size: float = Field(..., description="Size of the planted area in hectares")
    description: Optional[str] = Field(None, description="Additional description or notes about the crop")

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the crop")
    variety: Optional[str] = Field(None, description="Variety or cultivar of the crop")
    planting_date: Optional[datetime] = Field(None, description="Date when the crop was planted")
    expected_harvest_date: Optional[datetime] = Field(None, description="Expected harvest date")
    field_location: Optional[str] = Field(None, description="Location of the field where crop is planted")
    area_size: Optional[float] = Field(None, description="Size of the planted area in hectares")
    description: Optional[str] = Field(None, description="Additional description or notes about the crop")

class Crop(CropBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 