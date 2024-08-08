import asyncio
from uuid import UUID
from db.models.franchise import Franchise
from datetime import datetime, timedelta

from db.models.recipe import Recipe

async def update_franchise_status():
    while True:
        current_time = datetime.now().time()
        franchises = await Franchise.all()
        for franchise in franchises:
            if franchise.open_time <= current_time <= franchise.close_time:
                franchise.is_open = True
            else:
                franchise.is_open = False
            await franchise.save()
        await asyncio.sleep(60)  # Check every minute

