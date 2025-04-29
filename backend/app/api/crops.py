from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models.crop import Crop, CropCreate, CropUpdate
from ..models.user import User
from ..services.crop import CropService
from ..utils.auth import get_current_user

router = APIRouter(
    prefix="/crops",
    tags=["crops"]
)

@router.post("/", response_model=Crop)
async def create_crop(
    crop_data: CropCreate,
    current_user: User = Depends(get_current_user),
    crop_service: CropService = Depends()
):
    """Create a new crop."""
    return await crop_service.create_crop(crop_data, current_user.id)

@router.get("/", response_model=List[Crop])
async def get_crops(
    current_user: User = Depends(get_current_user),
    crop_service: CropService = Depends()
):
    """Get all crops associated with the current user."""
    return await crop_service.get_user_crops(current_user.id)

@router.get("/{crop_id}", response_model=Crop)
async def get_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    crop_service: CropService = Depends()
):
    """Get a specific crop by ID."""
    crop = await crop_service.get_crop(crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    if crop.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this crop"
        )
    return crop

@router.put("/{crop_id}", response_model=Crop)
async def update_crop(
    crop_id: int,
    crop_data: CropUpdate,
    current_user: User = Depends(get_current_user),
    crop_service: CropService = Depends()
):
    """Update a specific crop."""
    crop = await crop_service.get_crop(crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    if crop.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this crop"
        )
    return await crop_service.update_crop(crop_id, crop_data)

@router.delete("/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(
    crop_id: int,
    current_user: User = Depends(get_current_user),
    crop_service: CropService = Depends()
):
    """Delete a specific crop."""
    crop = await crop_service.get_crop(crop_id)
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Crop not found"
        )
    if crop.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this crop"
        )
    await crop_service.delete_crop(crop_id) 