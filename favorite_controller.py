from fastapi import APIRouter, HTTPException
from Service import favorite_service

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("/user/{user_id}")
async def get_user_favorites(user_id: int):
    return await favorite_service.get_user_favorites(user_id)

@router.post("/add")
async def add_to_favorites(favorite_data: dict):
    try:
        result = await favorite_service.add_to_favorites(
            favorite_data["user_id"],
            favorite_data["product_id"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/remove")
async def remove_from_favorites(favorite_data: dict):
    try:
        result = await favorite_service.remove_from_favorites(
            favorite_data["user_id"],
            favorite_data["product_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
