from typing import Optional
from pydantic import BaseModel
from Models.order_status import OrderStatus

class Order(BaseModel):
    OrderID: Optional[int] = None
    UserID: int
    OrderDate: str
    ShippingAddress: str
    TotalPrice: float
    OrderStatus: OrderStatus

