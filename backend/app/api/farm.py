from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.farm import Farm
from ..services.farm_service import FarmService
from .auth import get_current_user
from ..models.user import User

router = APIRouter()

@router.post("/farms/", response_model=Farm)
async def create_farm(
    farm_data: dict,
    current_user: User = Depends(get_current_user)
):
    return await FarmService.create_farm(farm_data, current_user)

@router.get("/farms/", response_model=List[Farm])
async def get_user_farms(current_user: User = Depends(get_current_user)):
    return await FarmService.get_farms_by_user(current_user.id)

@router.get("/farms/{farm_id}", response_model=Farm)
async def get_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user)
):
    farm = await FarmService.get_farm(farm_id)
    if not farm or farm.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm

@router.put("/farms/{farm_id}", response_model=Farm)
async def update_farm(
    farm_id: int,
    farm_data: dict,
    current_user: User = Depends(get_current_user)
):
    farm = await FarmService.get_farm(farm_id)
    if not farm or farm.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Farm not found")
    return await FarmService.update_farm(farm_id, farm_data)

@router.delete("/farms/{farm_id}")
async def delete_farm(
    farm_id: int,
    current_user: User = Depends(get_current_user)
):
    farm = await FarmService.get_farm(farm_id)
    if not farm or farm.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Farm not found")
    await FarmService.delete_farm(farm_id)
    return {"message": "Farm deleted successfully"} 