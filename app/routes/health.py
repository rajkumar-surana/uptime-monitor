from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
router= APIRouter()

@router.get("/health")
async def health_check(conn=Depends(get_db)):
    result = await conn.fetchval("select 1")
    return {"status": "ok", "db": result}