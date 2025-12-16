from database import database
from typing import List, Optional
from Models.order import Order
from Models.order_item import OrderItem
from Models.order_status import OrderStatus


async def get_order_by_id(order_id: int) -> Optional[dict]:
    q = "SELECT * FROM Orders WHERE OrderID=:order_id"
    return await database.fetch_one(q, values={"order_id": order_id})


async def get_orders_by_user(user_id: int) -> List[dict]:
    q = "SELECT * FROM Orders WHERE UserID=:user_id ORDER BY OrderDate DESC"
    return await database.fetch_all(q, values={"user_id": user_id})


async def get_temp_order_by_user(user_id: int) -> Optional[dict]:
    q = "SELECT * FROM Orders WHERE UserID=:user_id AND OrderStatus=:status"
    return await database.fetch_one(q, values={"user_id": user_id, "status": OrderStatus.TEMP.value})


async def get_order_items(order_id: int) -> List[dict]:
    q = """
        SELECT oi.OrderItemID, oi.OrderID, oi.ProductID, oi.Quantity, oi.Price,
               p.Name as ProductName
        FROM OrderItems oi
        JOIN Products p ON oi.ProductID = p.ProductID
        WHERE oi.OrderID = :order_id
        """
    return await database.fetch_all(q, values={"order_id": order_id})


async def create_order(order: Order) -> int:
    q = """
        INSERT INTO Orders 
            (UserID, OrderDate, ShippingAddress, TotalPrice, OrderStatus)
        VALUES (:user_id, :order_date, :shipping_address, :total_price, :order_status)
        """
    return await database.execute(q, values={
        "user_id": order.UserID,
        "order_date": order.OrderDate,
        "shipping_address": order.ShippingAddress,
        "total_price": order.TotalPrice,
        "order_status": order.OrderStatus.value
    })


async def add_item_to_order(order_id: int, product_id: int, quantity: int, price: float) -> int:
    # בדיקה אם הפריט כבר קיים בהזמנה
    existing = await database.fetch_one(
        "SELECT * FROM OrderItems WHERE OrderID=:order_id AND ProductID=:product_id",
        values={"order_id": order_id, "product_id": product_id}
    )

    if existing:
        # עדכון כמות
        q = """
            UPDATE OrderItems 
            SET Quantity = Quantity + :quantity
            WHERE OrderID=:order_id AND ProductID=:product_id
            """
        return await database.execute(q, values={
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity
        })
    else:
        # הוספה חדשה
        q = """
            INSERT INTO OrderItems (OrderID, ProductID, Quantity, Price)
            VALUES (:order_id, :product_id, :quantity, :price)
            """
        return await database.execute(q, values={
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "price": price
        })


async def remove_item_from_order(order_id: int, product_id: int) -> bool:
    q = "DELETE FROM OrderItems WHERE OrderID=:order_id AND ProductID=:product_id"
    result = await database.execute(q, values={"order_id": order_id, "product_id": product_id})
    return result > 0


async def update_order_total(order_id: int) -> bool:
    q = """
        UPDATE Orders 
        SET TotalPrice = (
            SELECT SUM(Price * Quantity) 
            FROM OrderItems 
            WHERE OrderID = :order_id
        )
        WHERE OrderID = :order_id
        """
    result = await database.execute(q, values={"order_id": order_id})
    return result > 0


async def close_order(order_id: int) -> bool:
    q = "UPDATE Orders SET OrderStatus=:status WHERE OrderID=:order_id"
    result = await database.execute(q, values={"order_id": order_id, "status": OrderStatus.CLOSE.value})
    return result > 0


async def delete_order(order_id: int) -> bool:
    # מחיקת פריטי ההזמנה קודם
    await database.execute("DELETE FROM OrderItems WHERE OrderID=:order_id", values={"order_id": order_id})
    # מחיקת ההזמנה
    q = "DELETE FROM Orders WHERE OrderID=:order_id"
    result = await database.execute(q, values={"order_id": order_id})
    return result > 0
