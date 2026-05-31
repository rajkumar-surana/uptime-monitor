import httpx
import app.core.database as db
import asyncio
    
async def run_checker():
    while(True):
        try:
            async with db.pool.acquire() as conn:
                monitors= await conn.fetch('SELECT * FROM monitors WHERE (EXTRACT(EPOCH FROM NOW() - last_checked_at) > interval_seconds OR last_checked_at IS NULL) AND is_active= True ')
                async with httpx.AsyncClient() as client:
                    for monitor in monitors:
                        try:
                            response=await client.get(monitor["url"], timeout=10, follow_redirects=True)
                        except Exception:
                            continue
                        time_ms= int(response.elapsed.total_seconds() * 1000)
                        await conn.execute('INSERT INTO check_results(monitor_id, status_code, response_time_ms) VALUES ($1, $2, $3)',monitor["id"], response.status_code, time_ms)
                        await conn.execute('UPDATE monitors SET last_checked_at=NOW() WHERE id=$1', monitor["id"])
                        if response.status_code >= 400 and monitor["webhook_url"]:
                            await client.post(monitor["webhook_url"], json={"status":response.status_code})
        except Exception:
            pass                   
        await asyncio.sleep(10)  # check every 10 seconds for due monitors

