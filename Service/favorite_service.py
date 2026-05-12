<<<<<<< HEAD
from Repository import favorite_repository
from typing import List, Optional

async def get_user_favorites(user_id: int) -> List[dict]:
    return await favorite_repository.get_user_favorites(user_id)

async def add_to_favorites(user_id: int, product_id: int) -> dict:
    result = await favorite_repository.add_to_favorites(user_id, product_id)
    if result is None:
        return {"message": "Item already in favorites"}
    return {"message": "Item added to favorites successfully"}

async def remove_from_favorites(user_id: int, product_id: int) -> dict:
    success = await favorite_repository.remove_from_favorites(user_id, product_id)
    if not success:
        raise ValueError("Item not found in favorites")
=======
from Repository import favorite_repository
from typing import List, Optional

async def get_user_favorites(user_id: int) -> List[dict]:
    return await favorite_repository.get_user_favorites(user_id)

async def add_to_favorites(user_id: int, product_id: int) -> dict:
    result = await favorite_repository.add_to_favorites(user_id, product_id)
    if result is None:
        return {"message": "Item already in favorites"}
    return {"message": "Item added to favorites successfully"}

async def remove_from_favorites(user_id: int, product_id: int) -> dict:
    success = await favorite_repository.remove_from_favorites(user_id, product_id)
    if not success:
        raise ValueError("Item not found in favorites")
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
    return {"message": "Item removed from favorites successfully"}