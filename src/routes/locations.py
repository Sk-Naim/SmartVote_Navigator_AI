from fastapi import APIRouter
from src.models.schemas import LocationRequest, LocationResponse
from src.services.google_maps import maps_service

router = APIRouter()

@router.get("/locations", response_model=LocationResponse)
async def get_polling_location(zip_code: str):
    """
    Returns the nearest polling station using the Maps API integration.
    """
    return await maps_service.get_nearest_polling_station(zip_code)
