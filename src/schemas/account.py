from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

Money = condecimal(max_digits=14, decimal_places=2)

class AccountCreate(BaseModel):
    number: str
    holder_name: str

class AccountOut(BaseModel):
    id: int
    number: str
    holder_name: str
    balance: int
    created_at: datetime

    class Config:
        orm_mode = True

class AccountList(BaseModel):
    accounts: list[AccountOut]
