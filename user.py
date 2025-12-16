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
    UserStatus: UserStatus