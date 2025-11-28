from src.models import tables
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError
from decimal import Decimal

async def list_transactions(account_id: int):
    q = tables.transactions.select().where(tables.transactions.c.account_id == account_id).order_by(tables.transactions.c.created_at.desc())
    rows = await database.fetch_all(q)
    return rows

async def create_transaction(account_id: int, tx_type: str, amount: Decimal, description: str | None = None):
    # validate positive amount
    if amount <= 0:
        raise BusinessError("Amount must be positive")

    # fetch account
    acct_q = tables.accounts.select().where(tables.accounts.c.id == account_id)
    account = await database.fetch_one(acct_q)
    if not account:
        raise AccountNotFoundError()

    # for withdraw check balance
    balance = Decimal(account["balance"])
    if tx_type == "withdraw" and balance < amount:
        raise BusinessError("Insufficient funds")

    # open transaction: insert transaction and update balance atomically
    async with database.transaction():
        ins = tables.transactions.insert().values(account_id=account_id, type=tx_type, amount=amount, description=description)
        await database.execute(ins)

        new_balance = balance + amount if tx_type == "deposit" else balance - amount
        upd = tables.accounts.update().where(tables.accounts.c.id == account_id).values(balance=new_balance)
        await database.execute(upd)

    return True
