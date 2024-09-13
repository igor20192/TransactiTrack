from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from . import crud
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    total_transactions = sum([len(user.transactions) for user in users])
    total_amount = sum([sum([t.amount for t in user.transactions]) for user in users])
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "users": users,
            "total_transactions": total_transactions,
            "total_amount": total_amount,
        },
    )
