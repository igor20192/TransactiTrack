from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TransactionBase(BaseModel):
    type: str
    amount: float


class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserId(BaseModel):
    id: int

    class Config:
        from_attributes = True


class User(UserBase):
    id: int
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True
