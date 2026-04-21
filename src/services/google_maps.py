import urllib.parse
from src.models.schemas import LocationResponse

class GoogleMapsService:
    async def get_nearest_polling_station(self, zip_code: str) -> LocationResponse:
        """
        Mock implementation of Google Civic / Maps API for finding polling locations.
        In production, this would call the Google Civic Information API.
        """
        # Mocking the response with specific overrides for requested regions
        if zip_code == "713101":
            encoded_query = urllib.parse.quote("polling stations in Burdwan, West Bengal")
            address_string = "Burdwan Town Hall Polling Center, Burdwan, West Bengal (713101)"
            dist = 0.8
        else:
            encoded_query = urllib.parse.quote(f"polling stations near {zip_code}")
            address_string = f"Community Center Polling Station, {zip_code}"
            dist = 1.2

        maps_url = f"https://www.google.com/maps/search/{encoded_query}"
        
        return LocationResponse(
            address=address_string,
            maps_url=maps_url,
            distance_miles=dist
        )

maps_service = GoogleMapsService()
