
from database import database
from typing import List, Optional
from Models.user import User
import hashlib


async def get_user_by_id(user_id: int) -> Optional[dict]:
    q = "SELECT * FROM Users WHERE UserID=:user_id"
    return await database.fetch_one(q, values={"user_id": user_id})


async def get_all_users() -> List[dict]:
    q = "SELECT * FROM Users"
    return await database.fetch_all(q)


async def get_user_by_email(email: str) -> Optional[dict]:
    q = "SELECT * FROM Users WHERE Email=:email"
    return await database.fetch_one(q, values={"email": email})


async def get_user_by_username(username: str) -> Optional[dict]:
    q = "SELECT * FROM Users WHERE Username=:username"
    return await database.fetch_one(q, values={"username": username})


async def create_user(user: User) -> int:
    # הצפנת סיסמה
    hashed_password = hashlib.sha256(user.Password.encode()).hexdigest()

    q = """
        INSERT INTO Users 
            (FirstName, LastName, Email, Phone, Country, City, Username, Password, UserStatus)
        VALUES (:first_name, :last_name, :email, :phone, :country, :city, :username, :password, :user_status)
        """
    return await database.execute(q, values={
        "first_name": user.FirstName,
        "last_name": user.LastName,
        "email": user.Email,
        "phone": user.Phone,
        "country": user.Country,
        "city": user.City,
        "username": user.Username,
        "password": hashed_password,
        "user_status": user.UserStatus.value
    })


async def update_user(user_id: int, user: User) -> bool:
    q = """
        UPDATE Users SET 
            FirstName=:first_name, LastName=:last_name, Email=:email, 
            Phone=:phone, Country=:country, City=:city
        WHERE UserID=:user_id
        """
    result = await database.execute(q, values={
        "user_id": user_id,
        "first_name": user.FirstName,
        "last_name": user.LastName,
        "email": user.Email,
        "phone": user.Phone,
        "country": user.Country,
        "city": user.City
    })
    return result > 0


async def delete_user(user_id: int) -> bool:
    q = "DELETE FROM Users WHERE UserID=:user_id"
    result = await database.execute(q, values={"user_id": user_id})
    return result > 0


async def verify_password(username: str, password: str) -> Optional[dict]:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    q = "SELECT * FROM Users WHERE Username=:username AND Password=:password"
    return await database.fetch_one(q, values={"username": username, "password": hashed_password})