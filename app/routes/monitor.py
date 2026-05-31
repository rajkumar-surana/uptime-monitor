from fastapi import APIRouter, Depends, Request, HTTPException
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.schema import monitorCreate, monitorUpdate
from app.services.monitor_service import registerMonitor, deleteMonitor, updateMonitor

router= APIRouter()

@router.post("/monitors")
async def new_monitor( body:monitorCreate, user_id= Depends(get_current_user), conn= Depends(get_db)):
    return await registerMonitor(body, conn, user_id)


@router.get("/monitors")
async def get_monitors(user_id=Depends(get_current_user), conn=Depends(get_db)):
    monitors = await conn.fetch('SELECT id from monitors WHERE user_id=$1',user_id)
    return [dict(row) for row in monitors]

@router.delete("/monitors/{id}")
async def delete_monitor(id:str, user_id= Depends(get_current_user), conn=Depends(get_db)):
    return await deleteMonitor(id, user_id, conn)

@router.patch("/monitors/{id}")
async def update_monitor(id:str, body: monitorUpdate, user_id=Depends(get_current_user), conn= Depends(get_db)):
    fields = body.model_dump(exclude_none=True)  # only fields that were sent
    if not fields:
        raise HTTPException(400, "Nothing to update")
    
    # Build SET clause dynamically
    return await updateMonitor(id, user_id, fields, conn)