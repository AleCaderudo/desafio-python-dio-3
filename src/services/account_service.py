from src.models import tables
from src.database import database
from decimal import Decimal

async def create_account(owner_id: int, number: str, holder_name: str):
    # check unique number
    q = tables.accounts.select().where(tables.accounts.c.number == number)
    exists = await database.fetch_one(q)
    if exists:
        raise ValueError("Account number already exists")
    ins = tables.accounts.insert().values(owner_id=owner_id, number=number, holder_name=holder_name, balance=Decimal("0.00"))
    account_id = await database.execute(ins)
    return account_id

async def list_accounts(owner_id: int):
    q = tables.accounts.select().where(tables.accounts.c.owner_id == owner_id)
    rows = await database.fetch_all(q)
    return rows

async def get_account_by_id(account_id: int):
    q = tables.accounts.select().where(tables.accounts.c.id == account_id)
    return await database.fetch_one(q)
