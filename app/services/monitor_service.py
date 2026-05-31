from app.models.schema import monitorCreate, monitorUpdate
from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse

async def registerMonitor( body: monitorCreate, conn, user_id ):

    if body.webhook_url==None:
        monitor_id=await conn.fetchrow('INSERT INTO monitors(user_id, url, interval_seconds) VALUES ($1, $2, $3) RETURNING id', user_id, body.url, body.interval_seconds)
    else:
        monitor_id=await conn.fetchrow('INSERT INTO monitors(user_id, url, interval_seconds, webhook_url) VALUES ($1, $2, $3, $4) RETURNING id', user_id, body.url, body.interval_seconds, body.webhook_url)
    
    return  JSONResponse({"id": str(monitor_id["id"])}, status_code=201)


async def deleteMonitor(monitor_id, user_id, conn):

    await conn.execute("DELETE FROM check_results WHERE monitor_id = $1", monitor_id)
    result = await conn.execute("DELETE FROM monitors WHERE id = $1 AND user_id = $2", monitor_id, user_id)

    if result == "DELETE 0":
        raise HTTPException(404, "Monitor not found")
    else:
        return Response(status_code=204)
    

async def updateMonitor(monitor_id, user_id, fields, conn):
    set_parts = []
    values = []
    for i, (key, val) in enumerate(fields.items(), start=1):
        set_parts.append(f"{key} = ${i}")
        values.append(val)
    
    query = f"UPDATE monitors SET {', '.join(set_parts)} WHERE id = ${len(values)+1} AND user_id = ${len(values)+2} RETURNING id"
    values.extend([monitor_id, user_id])
    
    result = await conn.fetchrow(query, *values)
    if not result:
        raise HTTPException(404, "Monitor not found")
    return Response(status_code=204)