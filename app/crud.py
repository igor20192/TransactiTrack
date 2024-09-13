from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, username: str):
    db_user = models.User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserId.from_orm(db_user)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def add_transaction(db: Session, user_id: int, type: str, amount: float):
    db_transaction = models.Transaction(user_id=user_id, type=type, amount=amount)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
