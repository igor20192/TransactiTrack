import logging
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from . import models, schemas

logger = logging.getLogger(__name__)


async def create_user(db: AsyncSession, username: str):
    """
    Asynchronously create a new user with the given username.

    Args:
        db (AsyncSession): The asynchronous database session.
        username (str): The username of the new user.

    Returns:
        schemas.UserId: The schema containing the user's ID.

    Raises:
        Exception: If an error occurs during user creation.
    """
    try:
        logger.debug(f"Creating new user: {username}")
        db_user = models.User(username=username)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"User created with ID: {db_user.id}")
        return schemas.UserId.model_validate(db_user)
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        raise


async def get_user(db: AsyncSession, user_id: int):
    """
    Asynchronously fetch a user by their ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user to fetch.

    Returns:
        models.User: The user model object if found, otherwise None.

    Raises:
        Exception: If an error occurs while fetching the user.
    """
    try:
        logger.debug(f"Fetching user with ID: {user_id}")
        result = await db.execute(
            select(models.User)
            .options(selectinload(models.User.transactions))  # Eager load transactions
            .where(models.User.id == user_id)
        )
        user = result.scalars().first()

        if user:
            logger.info(f"User found: {user.id}")
        else:
            logger.warning(f"User with ID {user_id} not found")
        return user
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {e}", exc_info=True)
        raise


async def get_all_users(db: AsyncSession):
    """
    Asynchronously fetch all users from the database, including their transactions.

    Args:
        db (AsyncSession): The asynchronous database session.

    Returns:
        List[models.User]: A list of user model objects.

    Raises:
        Exception: If an error occurs while fetching the users.
    """
    try:
        logger.debug("Fetching all users from the database")
        result = await db.execute(
            select(models.User).options(selectinload(models.User.transactions))
        )
        users = result.scalars().all()
        logger.info(f"Fetched {len(users)} users")
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {e}", exc_info=True)
        raise


async def add_transaction(db: AsyncSession, user_id: int, type: str, amount: float):
    """
    Asynchronously add a new transaction for a user.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user the transaction belongs to.
        type (str): The type of transaction (e.g., 'credit', 'debit').
        amount (float): The amount of the transaction.

    Returns:
        models.Transaction: The newly created transaction object.

    Raises:
        Exception: If an error occurs during transaction creation.
    """
    try:
        logger.debug(
            f"Adding transaction for user ID {user_id}: type={type}, amount={amount}"
        )
        db_transaction = models.Transaction(user_id=user_id, type=type, amount=amount)
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)
        logger.info(f"Transaction added with ID: {db_transaction.id}")
        return db_transaction
    except Exception as e:
        logger.error(
            f"Error adding transaction for user ID {user_id}: {e}", exc_info=True
        )
        raise


async def update_user(db: AsyncSession, user_id: int, username: str):
    """
    Asynchronously update a user's username by their ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user to update.
        username (str): The new username.

    Returns:
        models.User: The updated user object, or None if the user is not found.

    Raises:
        Exception: If an error occurs while updating the user.
    """
    try:
        logger.debug(f"Updating user ID {user_id} with new username: {username}")
        query = select(models.User).where(models.User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:
            update_query = (
                models.User.__table__.update()
                .where(models.User.id == user_id)
                .values(username=username)
            )
            await db.execute(update_query)
            await db.commit()
            logger.info(f"User ID {user_id} updated successfully")
            return user
        logger.warning(f"User with ID {user_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error updating user ID {user_id}: {e}", exc_info=True)
        raise


async def delete_user(db: AsyncSession, user_id: int):
    """
    Asynchronously delete a user and their associated transactions by their ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user to delete.

    Returns:
        int: The number of rows affected (1 if the user is deleted, 0 if not).

    Raises:
        Exception: If an error occurs during user deletion.
    """
    try:
        logger.debug(f"Deleting user with ID {user_id} and their transactions")
        async with db.begin():
            delete_transactions_query = delete(models.Transaction).where(
                models.Transaction.user_id == user_id
            )
            await db.execute(delete_transactions_query)

            delete_user_query = delete(models.User).where(models.User.id == user_id)
            result = await db.execute(delete_user_query)

            await db.commit()
        logger.info(f"User with ID {user_id} deleted")
        return result.rowcount
    except IntegrityError as e:
        logger.error(f"Integrity error during user deletion: {e}", exc_info=True)
        await db.rollback()
        return 0
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}", exc_info=True)
        await db.rollback()
        return 0


async def get_user_by_id(db: AsyncSession, user_id: int):
    """
    Asynchronously fetch a user by their ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user to fetch.

    Returns:
        models.User: The user object if found, otherwise None.

    Raises:
        Exception: If an error occurs while fetching the user.
    """
    try:
        logger.debug(f"Fetching user by ID {user_id}")
        query = select(models.User).where(models.User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()

        if user:
            logger.info(f"User with ID {user_id} found")
        else:
            logger.warning(f"User with ID {user_id} not found")
        return user
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}", exc_info=True)
        raise
