from pydantic import BaseModel, EmailStr
from datetime import datetime

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