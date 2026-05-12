<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel

class OrderItem(BaseModel):
    OrderItemID: Optional[int] = None
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float
=======
from typing import Optional
from pydantic import BaseModel

class OrderItem(BaseModel):
    OrderItemID: Optional[int] = None
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
