from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from . import crud, schemas
from .database import async_get_db
from .admin import router as admin_router

# Setting up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include the admin router for handling admin-related routes
app.include_router(admin_router)

# Serve static files from the "app/static" directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.post("/users/", response_model=schemas.UserId)
async def add_user(user: schemas.UserBase, db: AsyncSession = Depends(async_get_db)):
    """
    Create a new user in the database.

    This endpoint allows for creating a user by specifying a username.
    The user will be stored in the database, and its ID will be returned.

    Args:
        user (schemas.UserCreate): The request body containing the username of the user to be created.
        db (AsyncSession, optional): The database session, injected via FastAPI dependency.

    Returns:
        schemas.UserId: The created user's ID.

    Raises:
        HTTPException: If an error occurs during user creation, a 500 Internal Server Error is raised.
    """
    try:
        logger.debug(f"Creating user with username: {user.username}")
        new_user = await crud.create_user(db=db, username=user.username)
        logger.info(f"User created with ID: {new_user.id}")
        return new_user
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error creating user")


@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    """
    Retrieve a user by their ID from the database.

    This endpoint allows for fetching the details of a user by providing their user ID.

    Args:
        user_id (int): The ID of the user to be retrieved.
        db (AsyncSession, optional): The database session, injected via FastAPI dependency.

    Returns:
        schemas.User: The user details.

    Raises:
        HTTPException:
            - 404 Not Found if the user with the provided ID is not found.
            - 500 Internal Server Error if an error occurs during retrieval.
    """
    try:
        logger.debug(f"Fetching user with ID: {user_id}")
        db_user = await crud.get_user(db, user_id=user_id)
        if db_user is None:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        logger.info(f"User fetched with ID: {user_id}")
        return db_user
    except Exception as e:
        logger.error(f"Error fetching user: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching user")


@app.get("/users/", response_model=List[schemas.User])
async def get_all_users(db: AsyncSession = Depends(async_get_db)):
    """
    Retrieve all users from the database.

    This endpoint fetches and returns a list of all users in the database.

    Args:
        db (AsyncSession, optional): The database session, injected via FastAPI dependency.

    Returns:
        List[schemas.User]: A list of all users in the database.

    Raises:
        HTTPException: If an error occurs while fetching the users, a 500 Internal Server Error is raised.
    """
    try:
        logger.debug("Fetching all users")
        users = await crud.get_all_users(db)
        logger.info(f"Fetched {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error fetching all users: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error fetching users")


@app.post("/transactions/")
async def add_transaction(
    transaction: schemas.Transaction, db: AsyncSession = Depends(async_get_db)
):
    """
    Add a transaction for a specific user.

    This endpoint allows you to add a transaction for a user by specifying the user ID,
    the type of the transaction, and the amount.

    Args:
        transaction (schemas.Transaction): The request body containing the user ID,
            transaction type, and amount.
        db (AsyncSession, optional): The database session, injected via FastAPI dependency.

    Returns:
        models.Transaction: Details of the added transaction.

    Raises:
        HTTPException: Returns a 500 Internal Server Error if an error occurs during
            transaction creation.
    """
    try:
        logger.debug(
            f"Adding transaction for user ID {transaction.user_id}: type={transaction.type}, amount={transaction.amount}"
        )
        transaction_data = await crud.add_transaction(
            db=db,
            user_id=transaction.user_id,
            type=transaction.type,
            amount=transaction.amount,
        )
        logger.info(f"Transaction added with ID: {transaction_data.id}")
        return transaction_data
    except Exception as e:
        logger.error(f"Error adding transaction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error adding transaction")
