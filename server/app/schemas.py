from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
