import asyncio
from typing import List
from uuid import UUID
from db.models.recipe import Recipe
from db.models.franchise import Franchise

async def notify_franchises(franchises: List[Franchise], recipe: Recipe):
    # In a real-world scenario, you'd send notifications to franchises
    # This is a placeholder for demonstration purposes
    print(f"Notifying {len(franchises)} franchises about recipe {recipe.id}")

async def wait_for_recipe_acceptance(recipe_id: UUID, timeout: int = 300):
    start_time = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start_time < timeout:
        recipe = await Recipe.get(id=recipe_id).prefetch_related('franchise')
        if recipe.franchise:
            return recipe
        await asyncio.sleep(5)  # Check every 5 seconds
    return None