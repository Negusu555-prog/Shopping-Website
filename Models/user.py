<<<<<<< HEAD
from typing import Optional
from pydantic import BaseModel
from Models.user_status import UserStatus

class User(BaseModel):
    UserID: Optional[int] = None
    FirstName: str
    LastName: str
    Email: str
    Phone: int
    Country: str
    City: str
    Username: str
    Password: str
=======
from typing import Optional
from pydantic import BaseModel
from Models.user_status import UserStatus

class User(BaseModel):
    UserID: Optional[int] = None
    FirstName: str
    LastName: str
    Email: str
    Phone: int
    Country: str
    City: str
    Username: str
    Password: str
>>>>>>> 7222ba1b59b8f654c5bb751768b4493b1004fb18
    UserStatus: UserStatus