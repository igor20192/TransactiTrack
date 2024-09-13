from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

app = FastAPI()


# Зависимость для сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserId)
async def add_user(username: str, db: Session = Depends(get_db)):
    return crud.create_user(db=db, username=username)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db)


@app.post("/transactions/")
def add_transaction(
    user_id: int, type: str, amount: float, db: Session = Depends(get_db)
):
    return crud.add_transaction(db=db, user_id=user_id, type=type, amount=amount)
