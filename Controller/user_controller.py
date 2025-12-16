from fastapi import APIRouter, HTTPException, status
from Service import user_service
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
async def register_user(user_data: dict):
    try:
        result = await user_service.register_user(user_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(credentials: dict):
    user = await user_service.login_user(credentials["username"], credentials["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get("/")
async def get_all_users():
    return await user_service.get_all_users()

@router.get("/{user_id}")
async def get_user(user_id: int):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int):
    success = await user_service.delete_user_account(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}