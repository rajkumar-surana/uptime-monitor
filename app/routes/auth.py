from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.models.schema import authRequest
from app.core.security import hash_pwd, verify_pwd, create_token

router = APIRouter()


@router.post("/register")
async def register(body: authRequest, conn=Depends(get_db)):
    existing = await conn.fetchrow("SELECT id FROM users WHERE email = $1", body.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Already registered")

    hashed = hash_pwd(body.password)
    row = await conn.fetchrow(
        "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id",
        body.email, hashed
    )
    return {"token": create_token(str(row["id"]), body.email)}


@router.post("/login")
async def login(body: authRequest, conn=Depends(get_db)):
    row = await conn.fetchrow("SELECT id, password_hash FROM users WHERE email = $1", body.email)
    if row is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_pwd(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"token": create_token(str(row["id"]), body.email)}

