from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    ProductID: Optional[int] = None
    Name: str
    Price: float
    Stock: int