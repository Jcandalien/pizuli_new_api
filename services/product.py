from uuid import UUID
from db.models.animal import Animal
from db.models.meat import Meat
from db.models.recipe import Recipe

async def get_product_by_id(product_id: UUID):
    # Try to find the product in each model
    product = await Animal.get_or_none(id=product_id)
    if product:
        return product, 'animal'

    product = await Meat.get_or_none(id=product_id)
    if product:
        return product, 'meat'

    product = await Recipe.get_or_none(id=product_id)
    if product:
        return product, 'recipe'

    return None, None