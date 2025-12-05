from src.models import tables
from src.database import database
from src.security import hash_password, verify_password, create_access_token
from src.schemas.auth import UserCreate
import jwt
import uuid

async def create_user(payload: UserCreate):
    query = tables.users.select().where(tables.users.c.username == payload.username)
    existing = await database.fetch_one(query)
    if existing:
        raise ValueError("User already exists")

    insert = tables.users.insert().values(
        username=payload.username,
        password_hash=hash_password(payload.password)
    )
    result = await database.execute(insert)
    return result

async def authenticate_user(username: str, password: str):
    query = tables.users.select().where(tables.users.c.username == username)
    user = await database.fetch_one(query)
    if not user:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    # return minimal user dict
    return {"id": user["id"], "username": user["username"]}

async def create_token_for_user(username: str):
    # subject can be username
    token = create_access_token(user_id=username)
    return token

def create_access_token(subject: str) -> str:
    payload = {
        "sub": subject,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token
