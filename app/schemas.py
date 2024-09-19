from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class Transaction(BaseModel):
    user_id: int
    type: str
    amount: float
    timestamp: Optional[datetime] = None  # Make timestamp optional

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """
    Base schema for a user, defining the core attributes required for user-related actions.

    Attributes:
        username (str): The unique username of the user.
    """

    username: str


class UserId(BaseModel):
    """
    Schema for a user that only includes the user's ID.

    Attributes:
        id (int): The unique identifier of the user.
    """

    id: int

    class Config:
        """
        Pydantic configuration for enabling ORM mode, allowing attributes to be loaded from an ORM model.
        """

        from_attributes = True


class User(UserBase):
    """
    Schema for a user that extends UserBase and includes additional fields such as transactions.

    Attributes:
        id (int): The unique identifier of the user.
        transactions (List[Transaction]): A list of transactions associated with the user. Defaults to an empty list.
    """

    id: int
    transactions: List[Transaction] = []

    class Config:
        """
        Pydantic configuration for enabling ORM mode, allowing attributes to be loaded from an ORM model.
        """

        from_attributes = True
