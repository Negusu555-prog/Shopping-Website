from fastapi import APIRouter, HTTPException, Query
from Service import product_service
from typing import Optional, List

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def get_all_products():
    """קבלת כל המוצרים"""
    return await product_service.get_all_products()

@router.get("/stats")
async def get_products_stats():
    """קבלת סטטיסטיקות על המוצרים"""
    return await product_service.get_products_stats()

@router.get("/available")
async def get_available_products():
    """קבלת מוצרים זמינים בלבד"""
    return await product_service.get_available_products_only()

@router.get("/{product_id}")
async def get_product(product_id: int):
    """קבלת מוצר ספציפי"""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/search")
async def search_products(search_data: dict):
    """חיפוש מוצרים לפי קריטריונים שונים"""
    try:
        results = await product_service.search_products(search_data)
        return {
            "products": results,
            "count": len(results),
            "search_criteria": search_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Search error: {str(e)}")


@router.get("/price/range")
async def get_products_by_price(
        min_price: Optional[float] = Query(None, description="Minimum price"),
        max_price: Optional[float] = Query(None, description="Maximum price")
):
    """קבלת מוצרים לפי טווח מחירים (דרך query parameters)"""
    try:
        products = await product_service.get_products_by_price_range(min_price, max_price)
        return {
            "products": products,
            "count": len(products),
            "price_range": {"min": min_price, "max": max_price}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock/range")
async def get_products_by_stock(
        min_stock: Optional[int] = Query(None, description="Minimum stock"),
        max_stock: Optional[int] = Query(None, description="Maximum stock")
):
    """קבלת מוצרים לפי טווח מלאי (דרך query parameters)"""
    try:
        products = await product_service.get_products_by_stock_range(min_stock, max_stock)
        return {
            "products": products,
            "count": len(products),
            "stock_range": {"min": min_stock, "max": max_stock}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
async def create_product(product_data: dict):
    """יצירת מוצר חדש"""
    try:
        # ולידציה בסיסית
        required_fields = ["name", "price", "stock"]
        for field in required_fields:
            if field not in product_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

        # ולידציה של סוגי נתונים
        if not isinstance(product_data["price"], (int, float)) or product_data["price"] < 0:
            raise HTTPException(status_code=400, detail="Price must be a positive number")

        if not isinstance(product_data["stock"], int) or product_data["stock"] < 0:
            raise HTTPException(status_code=400, detail="Stock must be a non-negative integer")

        product_id = await product_service.create_product(product_data)
        return {
            "product_id": product_id,
            "message": "Product created successfully",
            "product_data": product_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Endpoint מיוחד לניהול מלאי (לעתיד)
@router.patch("/{product_id}/stock")
async def update_product_stock(product_id: int, stock_data: dict):
    """עדכון מלאי מוצר"""
    try:
        if "stock" not in stock_data:
            raise HTTPException(status_code=400, detail="Stock value is required")

        new_stock = stock_data["stock"]
        if not isinstance(new_stock, int) or new_stock < 0:
            raise HTTPException(status_code=400, detail="Stock must be a non-negative integer")

        success = await product_service.update_product_stock(product_id, new_stock)

        if not success:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Stock updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

