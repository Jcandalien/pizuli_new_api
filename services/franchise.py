from datetime import datetime, time
from typing import List
from db.models.franchise import Franchise
from utils.distance import haversine_distance

async def is_franchise_open(franchise: Franchise) -> bool:
    if franchise.is_paused:
        return False

    current_time = datetime.now().time()
    return franchise.is_open and franchise.open_time <= current_time <= franchise.close_time

async def get_nearest_open_franchises(lat: float, lon: float, limit: int = 5) -> List[Franchise]:
    franchises = await Franchise.all()
    open_franchises = [f for f in franchises if await is_franchise_open(f)]

    # Sort franchises by distance
    sorted_franchises = sorted(open_franchises, key=lambda f: haversine_distance(lat, lon, f.latitude, f.longitude))

    return sorted_franchises[:limit]