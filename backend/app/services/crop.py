from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from ..config.database import get_db
from ..models.database.crop import CropDB
from ..models.crop import CropCreate, CropUpdate

class CropService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def create_crop(self, crop_data: CropCreate, user_id: int) -> CropDB:
        """Create a new crop entry."""
        db_crop = CropDB(
            user_id=user_id,
            **crop_data.dict()
        )
        self.db.add(db_crop)
        self.db.commit()
        self.db.refresh(db_crop)
        return db_crop

    async def get_crop(self, crop_id: int) -> Optional[CropDB]:
        """Get a specific crop by ID."""
        return self.db.query(CropDB).filter(CropDB.id == crop_id).first()

    async def get_crops(self, skip: int = 0, limit: int = 100) -> List[CropDB]:
        return self.db.query(CropDB).offset(skip).limit(limit).all()

    async def get_user_crops(self, user_id: int) -> List[CropDB]:
        """Get all crops for a specific user."""
        return self.db.query(CropDB).filter(CropDB.user_id == user_id).all()

    async def update_crop(self, crop_id: int, crop_data: CropUpdate) -> CropDB:
        """Update a specific crop."""
        db_crop = await self.get_crop(crop_id)
        if not db_crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found"
            )

        update_data = crop_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_crop, field, value)

        db_crop.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_crop)
        return db_crop

    async def delete_crop(self, crop_id: int) -> None:
        """Delete a specific crop."""
        db_crop = await self.get_crop(crop_id)
        if not db_crop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Crop not found"
            )

        self.db.delete(db_crop)
        self.db.commit() 