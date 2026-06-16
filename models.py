from pydantic import BaseModel, field_validator
from typing import Literal
from pydantic import Field
from datetime import datetime
import uuid

class Transaction(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    amount: float
    category: str
    type: Literal["income", "expense"]
    description: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator('amount')
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be positive")
        return v

    @field_validator('category')
    @classmethod
    def normalize_category(cls, v):
        return v.lower().strip()


class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username : str 
    password : str
    name : str
    balance : float = 0.0
    budget : float = 0.0
    age : int
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 0:
            raise ValueError("age cannot be negative")
        if v > 150:
            raise ValueError("age cannot be over 150")
        return v
    
    @field_validator('username')
    @classmethod
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError("username must be at least 3 characters long")
        if len(v) > 20:
            raise ValueError("username must be at most 20 characters long")
        if " " in v:
            raise ValueError("username cannot contain spaces")
        return v
    

t1 = Transaction(user_id="draven", amount=500, category="Food", type="expense")
print(t1)


