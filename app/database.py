from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

user = config("DATABASE_USERNAME")
password = config("DATABASE_PASSWORD")
mydatabase = config("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@localhost/{mydatabase}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
