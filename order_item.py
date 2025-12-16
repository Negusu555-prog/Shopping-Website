from typing import Optional
from pydantic import BaseModel

class OrderItem(BaseModel):
    OrderItemID: Optional[int] = None
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float
