from pydantic import BaseModel, condecimal, Field
from typing import Optional
from datetime import datetime

Money = condecimal(max_digits=14, decimal_places=2)

class TransactionCreate(BaseModel):
    account_id: int
    type: str = Field(..., regex="^(credit|debit)$")
    amount: Money
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: Money
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
