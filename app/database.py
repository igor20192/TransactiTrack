from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Obtaining connection data from environment variables
user = config("DATABASE_USERNAME")
password = config("DATABASE_PASSWORD")
mydatabase = config("DATABASE_NAME")

# Asynchronous URL for connecting to PostgreSQL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{user}:{password}@localhost/{mydatabase}"
)

# Creating an asynchronous database engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Creating a session factory for asynchronous requests
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Basic class for models
Base = declarative_base()


#  Asynchronous session generator for database operations
async def async_get_db():
    """
    Asynchronous generator that creates a new session for performing database operations.

    This generator creates a session for each request using the session factory `SessionLocal`.
    The session is used to perform read and write operations on the database. Once the request
    is completed, the session is automatically closed.

    This is commonly used in FastAPI or other asynchronous frameworks to provide a database session
    for request handling.

    Example usage:
        async def some_view_function(db: AsyncSession = Depends(async_get_db)):
            # Use the `db` object to interact with the database.
            ...

    Yields:
        AsyncSession: An asynchronous session to interact with the database.
    """
    async with SessionLocal() as session:
        yield session
