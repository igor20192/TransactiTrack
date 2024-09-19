from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TransactionBase(BaseModel):
    """
    Base schema for a transaction. It defines the common attributes for creating or interacting with transactions.

    Attributes:
        type (str): The type of transaction (e.g., 'credit', 'debit').
        amount (float): The amount of money involved in the transaction.
    """

    type: str
    amount: float


class Transaction(TransactionBase):
    """
    Schema for a transaction that extends the TransactionBase schema with additional attributes.

    Attributes:
        id (int): The unique identifier of the transaction.
        timestamp (datetime): The time when the transaction occurred.
    """

    id: int
    timestamp: datetime

    class Config:
        """
        Pydantic configuration for enabling ORM mode, allowing attributes to be loaded from an ORM model.
        """

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
