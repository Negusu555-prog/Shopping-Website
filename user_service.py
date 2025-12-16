from typing import List, Optional
from Repository import user_repository
from Models.user import User
from Models.user_status import UserStatus


async def get_all_users() -> List[dict]:
    return await user_repository.get_all_users()


async def get_user_by_id(user_id: int) -> Optional[dict]:
    return await user_repository.get_user_by_id(user_id)


async def get_user_by_email(email: str) -> Optional[dict]:
    return await user_repository.get_user_by_email(email)


async def register_user(user_data: dict) -> dict:
    # בדיקה שהמשתמש לא קיים
    existing_user = await user_repository.get_user_by_username(user_data["username"])
    if existing_user:
        raise ValueError("Username already exists")

    existing_email = await user_repository.get_user_by_email(user_data["email"])
    if existing_email:
        raise ValueError("Email already exists")

    user = User(
        FirstName=user_data["first_name"],
        LastName=user_data["last_name"],
        Email=user_data["email"],
        Phone=user_data["phone"],
        Country=user_data["country"],
        City=user_data["city"],
        Username=user_data["username"],
        Password=user_data["password"],
        UserStatus=UserStatus.REGISTER
    )

    user_id = await user_repository.create_user(user)
    return {"user_id": user_id, "message": "User registered successfully"}


async def login_user(username: str, password: str) -> Optional[dict]:
    user = await user_repository.verify_password(username, password)
    if user:
        return {
            "user_id": user["UserID"],
            "username": user["Username"],
            "first_name": user["FirstName"],
            "last_name": user["LastName"]
        }
    return None


async def delete_user_account(user_id: int) -> bool:
    return await user_repository.delete_user(user_id)
