from fastapi import APIRouter, Form, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from decouple import config
from . import crud
from .database import async_get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Load templates from the directory specified in the configuration file
templates = Jinja2Templates(directory=config("PATH_TEMPLATES"))


@router.get("/admin/")
async def admin_dashboard(request: Request, db: AsyncSession = Depends(async_get_db)):
    """
    Displays the admin dashboard with user and transaction information.

    Fetches all user data, calculates the total number of transactions, and the total amount,
    and passes this information to the template for rendering in the browser.

    Args:
        request (Request): HTTP request object containing user request data.
        db (AsyncSession): Asynchronous database session for performing CRUD operations.

    Returns:
        TemplateResponse: A response containing the rendered template with user and transaction data.
    """
    users = await crud.get_all_users(db)  # Asynchronously retrieve all users

    # Create a list of user data
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "transaction_count": len(user.transactions),
        }
        for user in users
    ]

    # Calculate the total number of transactions and total amount
    total_transactions = sum([len(user.transactions) for user in users])
    total_amount = sum([sum([t.amount for t in user.transactions]) for user in users])

    # Prepare transaction data for chart generation
    transaction_data = {
        "dates": [t.timestamp.isoformat() for user in users for t in user.transactions],
        "amounts": [t.amount for user in users for t in user.transactions],
    }

    return templates.TemplateResponse(
        "list_users.html",
        {
            "request": request,
            "users": users_data,
            "total_transactions": total_transactions,
            "total_amount": total_amount,
            "transaction_data": transaction_data,  # Pass data for the chart
        },
    )


@router.get("/admin/users/{user_id}")
async def edit_user(
    user_id: int, request: Request, db: AsyncSession = Depends(async_get_db)
):
    """
    Loads the user edit page for a specific user by their ID.

    If the user is not found, returns a 404 error.

    Args:
        user_id (int): The ID of the user to be edited.
        request (Request): HTTP request object.
        db (AsyncSession): Asynchronous database session.

    Returns:
        TemplateResponse: A response containing the rendered template for user editing.

    Raises:
        HTTPException: If the user with the specified ID is not found.
    """
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "edit_user.html", {"request": request, "user": user}
    )


@router.post("/admin/users/{user_id}")
async def update_user(
    user_id: int, username: str = Form(...), db: AsyncSession = Depends(async_get_db)
):
    """
    Updates the username of a user by their ID.

    Retrieves the new username from the form and updates the record in the database.

    Args:
        user_id (int): The ID of the user to be updated.
        username (str): The new username retrieved from the form.
        db (AsyncSession): Asynchronous database session.

    Returns:
        RedirectResponse: Redirects to the admin dashboard after the update.
    """
    await crud.update_user(db, user_id, username)
    return RedirectResponse("/admin/", status_code=302)


@router.post("/admin/users/{user_id}/delete")
async def delete_user(user_id: int, db: AsyncSession = Depends(async_get_db)):
    """
    Deletes a user by their ID.

    If the deletion is successful, redirects back to the admin dashboard.

    Args:
        user_id (int): The ID of the user to be deleted.
        db (AsyncSession): Asynchronous database session.

    Returns:
        RedirectResponse: Redirects to the admin dashboard after deletion.
    """
    await crud.delete_user(db, user_id)
    return RedirectResponse("/admin/", status_code=302)
