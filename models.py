from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    phone: str
    password: str
    email: Optional[str] = None
    firstName: str
    lastName: Optional[str] = None
    gender: str
    dob: str = '01/01/1900' 
    location: Optional[str] = None
    timestamp: datetime = datetime.now()
    updatedBy: str = 'api'