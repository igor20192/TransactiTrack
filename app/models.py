from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Base class for all ORM models
Base = declarative_base()


class User(Base):
    """
    ORM model representing a user in the system.

    Attributes:
        id (int): The primary key for the user table.
        username (str): The username of the user. It must be unique.
        transactions (List[Transaction]): A relationship to the Transaction table,
            indicating the transactions associated with this user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    transactions = relationship("Transaction", back_populates="user")


class Transaction(Base):
    """
    ORM model representing a transaction for a user.

    Attributes:
        id (int): The primary key for the transaction table.
        user_id (int): Foreign key linking to the user who made the transaction.
        type (str): The type of the transaction (e.g., 'credit', 'debit').
        amount (float): The amount involved in the transaction.
        timestamp (datetime): The time when the transaction was created. Defaults to the current timestamp.
        user (User): A relationship to the User table, representing the user associated with this transaction.
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    user = relationship("User", back_populates="transactions")
