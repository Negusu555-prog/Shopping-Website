from fastapi import APIRouter, HTTPException
from Service import order_service

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/user/{user_id}")
async def get_user_orders(user_id: int):
    return await order_service.get_user_orders(user_id)

@router.get("/{order_id}/user/{user_id}")
async def get_order_details(order_id: int, user_id: int):
    order = await order_service.get_order_details(order_id, user_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/add-item")
async def add_item_to_order(order_data: dict):
    try:
        result = await order_service.add_item_to_temp_order(
            order_data["user_id"],
            order_data["product_id"],
            order_data["quantity"],
            order_data["shipping_address"]
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/remove-item")
async def remove_item_from_order(order_data: dict):
    try:
        result = await order_service.remove_item_from_temp_order(
            order_data["user_id"],
            order_data["product_id"]
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/{user_id}")
async def purchase_order(user_id: int):
    try:
        result = await order_service.purchase_order(user_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
