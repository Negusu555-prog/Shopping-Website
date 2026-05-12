<<<<<<< HEAD
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

=======
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

>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
