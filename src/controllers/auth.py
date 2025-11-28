from fastapi import APIRouter, HTTPException, status, Depends
from src.schemas.auth import UserCreate
from src.services.auth_service import create_user, authenticate_user
from src.security import sign_jwt  # <-- seu security.py

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate):
    try:
        await create_user(payload)
        return {"msg": "user created"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login")
async def login(payload: UserCreate):
    user = await authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = sign_jwt(user_id=user["id"])
    # sign_jwt retorna {"access_token": "<token>"} segundo seu arquivo
    return token
