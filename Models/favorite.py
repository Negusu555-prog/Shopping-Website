from typing import Optional
from pydantic import BaseModel

class Favorite(BaseModel):
    FavoriteID: Optional[int] = None
    UserID: int
    ProductID: int
