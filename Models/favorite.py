<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel

class Favorite(BaseModel):
    FavoriteID: Optional[int] = None
    UserID: int
    ProductID: int
=======
from typing import Optional
from pydantic import BaseModel

class Favorite(BaseModel):
    FavoriteID: Optional[int] = None
    UserID: int
    ProductID: int
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
