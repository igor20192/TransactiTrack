"""create users and transactions tables

Revision ID: d76f9ec9b3de
Revises: 
Create Date: 2024-09-12 21:43:39.752782

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d76f9ec9b3de"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(255), nullable=False, unique=True, index=True),
    )

    # Создание таблицы transactions
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.String(255), nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column(
            "timestamp", sa.DateTime, server_default=sa.func.now(), nullable=False
        ),
    )


def downgrade() -> None:

    # Удаление таблицы transactions
    op.drop_table("transactions")

    # Удаление таблицы users
    op.drop_table("users")
