<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    ProductID: Optional[int] = None
    Name: str
    Price: float
=======
from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    ProductID: Optional[int] = None
    Name: str
    Price: float
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
    Stock: int