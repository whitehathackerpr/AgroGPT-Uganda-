from datetime import datetime
from sqlalchemy.orm import Session
from ..models.farm import Farm
from ..models.user import User
from typing import List, Optional

class FarmService:
    @staticmethod
    async def create_farm(farm_data: dict, user: User) -> Farm:
        farm = Farm(
            user_id=user.id,
            name=farm_data["name"],
            location=farm_data["location"],
            size_hectares=farm_data["size_hectares"],
            main_crops=farm_data["main_crops"],
            soil_type=farm_data.get("soil_type"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        # Add to database session and commit
        return farm

    @staticmethod
    async def get_farms_by_user(user_id: int) -> List[Farm]:
        # Query farms by user_id
        return []

    @staticmethod
    async def get_farm(farm_id: int) -> Optional[Farm]:
        # Query farm by id
        return None

    @staticmethod
    async def update_farm(farm_id: int, farm_data: dict) -> Farm:
        farm = await FarmService.get_farm(farm_id)
        if farm:
            for key, value in farm_data.items():
                if hasattr(farm, key):
                    setattr(farm, key, value)
            farm.updated_at = datetime.utcnow()
            # Update in database
            return farm
        return None

    @staticmethod
    async def delete_farm(farm_id: int) -> bool:
        farm = await FarmService.get_farm(farm_id)
        if farm:
            # Delete from database
            return True
        return False 