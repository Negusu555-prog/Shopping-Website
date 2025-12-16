from database import database
from typing import List, Optional
from Models.product import Product


async def get_product_by_id(product_id: int) -> Optional[dict]:
    q = "SELECT * FROM Products WHERE ProductID=:product_id"
    return await database.fetch_one(q, values={"product_id": product_id})


async def get_all_products() -> List[dict]:
    q = "SELECT * FROM Products"
    return await database.fetch_all(q)


async def search_products_by_name(search_term: str) -> List[dict]:
    q = "SELECT * FROM Products WHERE Name LIKE :search_term"
    return await database.fetch_all(q, values={"search_term": f"%{search_term}%"})


async def search_products_by_multiple_terms(search_terms: List[str]) -> List[dict]:
    conditions = []
    values = {}
    for i, term in enumerate(search_terms):
        conditions.append(f"Name LIKE :term_{i}")
        values[f"term_{i}"] = f"%{term}%"

    q = f"SELECT * FROM Products WHERE {' OR '.join(conditions)}"
    return await database.fetch_all(q, values=values)


async def search_products_by_price_range(min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[
    dict]:
    conditions = []
    values = {}

    if min_price is not None:
        conditions.append("Price >= :min_price")
        values["min_price"] = min_price
    if max_price is not None:
        conditions.append("Price <= :max_price")
        values["max_price"] = max_price

    if conditions:
        q = f"SELECT * FROM Products WHERE {' AND '.join(conditions)}"
        return await database.fetch_all(q, values=values)
    else:
        return await get_all_products()


async def search_products_by_stock_range(min_stock: Optional[int] = None, max_stock: Optional[int] = None) -> List[
    dict]:
    conditions = []
    values = {}

    if min_stock is not None:
        conditions.append("Stock >= :min_stock")
        values["min_stock"] = min_stock
    if max_stock is not None:
        conditions.append("Stock <= :max_stock")
        values["max_stock"] = max_stock

    if conditions:
        q = f"SELECT * FROM Products WHERE {' AND '.join(conditions)}"
        return await database.fetch_all(q, values=values)
    else:
        return await get_all_products()


async def create_product(product: Product) -> int:
    q = """
        INSERT INTO Products 
            (Name, Price, Stock)
        VALUES (:name, :price, :stock)
        """
    return await database.execute(q, values={
        "name": product.Name,
        "price": product.Price,
        "stock": product.Stock
    })


async def update_product_stock(product_id: int, new_stock: int) -> bool:
    q = "UPDATE Products SET Stock=:stock WHERE ProductID=:product_id"
    result = await database.execute(q, values={"product_id": product_id, "stock": new_stock})
    return result > 0


async def decrease_stock(product_id: int, quantity: int) -> bool:
    q = """
        UPDATE Products 
        SET Stock = Stock - :quantity 
        WHERE ProductID=:product_id AND Stock >= :quantity
        """
    result = await database.execute(q, values={"product_id": product_id, "quantity": quantity})
    return result > 0