from src.database import metadata, engine
import sqlalchemy as sa
from datetime import datetime

# Users (for auth)
users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("username", sa.String(150), unique=True, nullable=False),
    sa.Column("password_hash", sa.String(256), nullable=False),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)

# Accounts
accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    sa.Column("number", sa.String(50), unique=True, nullable=False),
    sa.Column("holder_name", sa.String(200), nullable=False),
    sa.Column("balance", sa.Numeric(14, 2), nullable=False, server_default="0.00"),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)

# Transactions
transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("account_id", sa.Integer, sa.ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False),
    sa.Column("type", sa.Enum("deposit", "withdraw", name="transaction_type"), nullable=False),
    sa.Column("amount", sa.Numeric(14, 2), nullable=False),
    sa.Column("description", sa.String(500), nullable=True),
    sa.Column("created_at", sa.DateTime, default=datetime.utcnow),
)
