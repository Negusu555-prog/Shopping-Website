from typing import List, Optional
from Repository import product_repository
from Models.product import Product


async def get_all_products() -> List[dict]:
    return await product_repository.get_all_products()

async def get_product_by_id(product_id: int) -> Optional[dict]:
    return await product_repository.get_product_by_id(product_id)

async def search_products(search_data: dict) -> List[dict]:
    """
    חיפוש מוצרים לפי קריטריונים שונים
    """
    # חיפוש לפי שם/שמות
    if "names" in search_data and search_data["names"]:
        if isinstance(search_data["names"], list):
            return await product_repository.search_products_by_multiple_terms(search_data["names"])
        else:
            return await product_repository.search_products_by_name(search_data["names"])

    # חיפוש משולב - מחיר ומלאי
    if any(key in search_data for key in ["min_price", "max_price", "min_stock", "max_stock"]):
        return await search_products_advanced(search_data)

    # אם אין קריטריונים - החזר הכל
    return await product_repository.get_all_products()


async def search_products_advanced(search_data: dict) -> List[dict]:
    """
    חיפוש מתקדם שמשלב מחיר ומלאי
    """
    # קבלת כל המוצרים
    all_products = await product_repository.get_all_products()

    # סינון לפי הקריטריונים
    filtered_products = []

    for product in all_products:
        # בדיקת מחיר מינימלי
        if "min_price" in search_data:
            if product["Price"] < search_data["min_price"]:
                continue

        # בדיקת מחיר מקסימלי
        if "max_price" in search_data:
            if product["Price"] > search_data["max_price"]:
                continue

        # בדיקת מלאי מינימלי
        if "min_stock" in search_data:
            if product["Stock"] < search_data["min_stock"]:
                continue

        # בדיקת מלאי מקסימלי
        if "max_stock" in search_data:
            if product["Stock"] > search_data["max_stock"]:
                continue

        # אם עבר את כל הבדיקות - הוסף לרשימה
        filtered_products.append(product)

    return filtered_products


async def create_product(product_data: dict) -> int:
    product = Product(
        Name=product_data["name"],
        Price=product_data["price"],
        Stock=product_data["stock"]
    )
    return await product_repository.create_product(product)


# פונקציות עזר נוספות
async def get_products_by_price_range(min_price: float = None, max_price: float = None) -> List[dict]:
    """קבלת מוצרים לפי טווח מחירים"""
    return await product_repository.search_products_by_price_range(min_price, max_price)


async def get_products_by_stock_range(min_stock: int = None, max_stock: int = None) -> List[dict]:
    """קבלת מוצרים לפי טווח מלאי"""
    return await product_repository.search_products_by_stock_range(min_stock, max_stock)


async def get_available_products_only() -> List[dict]:
    """קבלת מוצרים זמינים בלבד (מלאי > 0)"""
    return await get_products_by_stock_range(min_stock=1)


async def get_products_stats() -> dict:
    """קבלת סטטיסטיקות על המוצרים"""
    products = await get_all_products()

    if not products:
        return {
            "total_products": 0,
            "available_products": 0,
            "out_of_stock": 0,
            "average_price": 0,
            "total_stock_value": 0
        }

    available_products = [p for p in products if p["Stock"] > 0]
    out_of_stock = [p for p in products if p["Stock"] == 0]

    total_prices = sum(p["Price"] for p in products)
    average_price = total_prices / len(products)

    total_stock_value = sum(p["Price"] * p["Stock"] for p in products)

    return {
        "total_products": len(products),
        "available_products": len(available_products),
        "out_of_stock": len(out_of_stock),
        "average_price": round(average_price, 2),
        "total_stock_value": round(total_stock_value, 2)
    }
#מעדכן את כמות המלאי של מוצר מסוים לפי מזהה המוצר
async def update_product_stock(product_id: int, new_stock: int) -> bool:
    return await product_repository.update_product_stock(product_id, new_stock)
