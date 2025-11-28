from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.account import AccountCreate, AccountOut
from src.services.account_service import create_account, list_accounts, get_account_by_id
from src.security import get_current_user  # <- dependency do seu security.py
from src.database import database

router = APIRouter(prefix="/accounts", tags=["account"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_account_endpoint(payload: AccountCreate, current_user: dict = Depends(get_current_user)):
    owner_id = current_user["user_id"]
    try:
        account_id = await create_account(owner_id=owner_id, number=payload.number, holder_name=payload.holder_name)
        return {"id": account_id}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/", response_model=list[AccountOut])
async def list_accounts_endpoint(current_user: dict = Depends(get_current_user)):
    owner_id = current_user["user_id"]
    rows = await list_accounts(owner_id)
    return rows

@router.get("/{account_id}", response_model=AccountOut)
async def get_account_endpoint(account_id: int, current_user: dict = Depends(get_current_user)):
    acct = await get_account_by_id(account_id)
    if not acct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    if acct["owner_id"] != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return acct
