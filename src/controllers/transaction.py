from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.transaction import TransactionCreate, TransactionOut
from src.services.transaction import create_transaction, list_transactions
from src.security import get_current_user
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError

router = APIRouter(prefix="/transactions", tags=["transaction"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transaction_endpoint(payload: TransactionCreate, current_user: dict = Depends(get_current_user)):
    # check account exists and owner
    acct_row = await database.fetch_one("SELECT owner_id FROM accounts WHERE id = :account_id", values={"account_id": payload.account_id})
    if not acct_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    if acct_row["owner_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    try:
        await create_transaction(account_id=payload.account_id, tx_type=payload.type, amount=payload.amount, description=payload.description)
        return {"msg": "transaction created"}
    except AccountNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except BusinessError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/account/{account_id}", response_model=list[TransactionOut])
async def get_account_transactions(account_id: int, current_user: dict = Depends(get_current_user)):
    acct_row = await database.fetch_one("SELECT owner_id FROM accounts WHERE id = :account_id", values={"account_id": account_id})
    if not acct_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    if acct_row["owner_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    rows = await list_transactions(account_id)
    return rows
