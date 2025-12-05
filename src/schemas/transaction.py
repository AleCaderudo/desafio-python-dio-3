from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    account_id: int
    type: str = Field(..., pattern="^(credit|debit)$")
    amount: Decimal = Field(..., max_digits=14, decimal_places=2)
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    account_id: int
    type: str
    amount: Decimal
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
