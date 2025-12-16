from database import database
from typing import List, Optional
from Models.favorite import Favorite


async def get_user_favorites(user_id: int) -> List[dict]:
    q = """
        SELECT f.FavoriteID, f.UserID, f.ProductID, p.Name, p.Price, p.Stock
        FROM Favorites f
        JOIN Products p ON f.ProductID = p.ProductID
        WHERE f.UserID = :user_id
        """
    return await database.fetch_all(q, values={"user_id": user_id})


async def add_to_favorites(user_id: int, product_id: int) -> Optional[int]:
    # בדיקה שהפריט לא כבר ברשימה
    existing = await database.fetch_one(
        "SELECT * FROM Favorites WHERE UserID=:user_id AND ProductID=:product_id",
        values={"user_id": user_id, "product_id": product_id}
    )

    if existing:
        return None  # כבר קיים

    q = "INSERT INTO Favorites (UserID, ProductID) VALUES (:user_id, :product_id)"
    return await database.execute(q, values={"user_id": user_id, "product_id": product_id})


async def remove_from_favorites(user_id: int, product_id: int) -> bool:
    q = "DELETE FROM Favorites WHERE UserID=:user_id AND ProductID=:product_id"
    result = await database.execute(q, values={"user_id": user_id, "product_id": product_id})
    return result > 0