from typing import List, Optional
from Repository import order_repository, product_repository
from Models.order import Order
from Models.order_status import OrderStatus
from datetime import datetime


async def get_user_orders(user_id: int) -> List[dict]:
    return await order_repository.get_orders_by_user(user_id)


async def get_order_details(order_id: int, user_id: int) -> Optional[dict]:
    order = await order_repository.get_order_by_id(order_id)
    if not order or order["UserID"] != user_id:
        return None

    items = await order_repository.get_order_items(order_id)
    return {
        "order": order,
        "items": items
    }


async def get_or_create_temp_order(user_id: int, shipping_address: str) -> dict:
    temp_order = await order_repository.get_temp_order_by_user(user_id)

    if temp_order:
        return temp_order

    # יצירת הזמנה זמנית חדשה
    order = Order(
        UserID=user_id,
        OrderDate=datetime.now().isoformat(),
        ShippingAddress=shipping_address,
        TotalPrice=0.0,
        OrderStatus=OrderStatus.TEMP
    )

    order_id = await order_repository.create_order(order)
    return await order_repository.get_order_by_id(order_id)


async def add_item_to_temp_order(user_id: int, product_id: int, quantity: int, shipping_address: str) -> dict:
    # בדיקת מלאי
    product = await product_repository.get_product_by_id(product_id)
    if not product or product["Stock"] < quantity:
        raise ValueError("Insufficient stock")

    # קבלת/יצירת הזמנה זמנית
    temp_order = await get_or_create_temp_order(user_id, shipping_address)

    # הוספת פריט
    await order_repository.add_item_to_order(
        temp_order["OrderID"],
        product_id,
        quantity,
        product["Price"]
    )

    # עדכון סך הכל
    await order_repository.update_order_total(temp_order["OrderID"])

    return {"message": "Item added to order successfully"}


async def remove_item_from_temp_order(user_id: int, product_id: int) -> dict:
    temp_order = await order_repository.get_temp_order_by_user(user_id)
    if not temp_order:
        raise ValueError("No temp order found")

    success = await order_repository.remove_item_from_order(temp_order["OrderID"], product_id)
    if not success:
        raise ValueError("Item not found in order")

    # עדכון סך הכל
    await order_repository.update_order_total(temp_order["OrderID"])

    # בדיקה אם ההזמנה ריקה
    items = await order_repository.get_order_items(temp_order["OrderID"])
    if not items:
        await order_repository.delete_order(temp_order["OrderID"])
        return {"message": "Order deleted - no items remaining"}

    return {"message": "Item removed from order successfully"}


async def purchase_order(user_id: int) -> dict:
    temp_order = await order_repository.get_temp_order_by_user(user_id)
    if not temp_order:
        raise ValueError("No temp order found")

    # קבלת פריטי ההזמנה
    items = await order_repository.get_order_items(temp_order["OrderID"])
    if not items:
        raise ValueError("Order is empty")

    # בדיקת מלאי וחישוב מחיר מעודכן
    total_price = 0
    for item in items:
        product = await product_repository.get_product_by_id(item["ProductID"])
        if not product or product["Stock"] < item["Quantity"]:
            raise ValueError(f"Insufficient stock for {item['ProductName']}")

        # הקטנת מלאי
        await product_repository.decrease_stock(item["ProductID"], item["Quantity"])
        total_price += item["Price"] * item["Quantity"]

    # סגירת ההזמנה
    await order_repository.close_order(temp_order["OrderID"])

    return {"message": "Order purchased successfully", "total_price": total_price}
