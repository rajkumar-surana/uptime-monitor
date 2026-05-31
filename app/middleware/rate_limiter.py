from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.database import get_redis

r= get_redis()
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        ip=request.client.host
        key= f"rateLimit:{ip}"
        counter= r.incr(key)
        if(counter==1):
            r.expire(key, 60)
        if(counter>10):
            return JSONResponse(status_code=429, content={"detail": "Too many requests, wait a minute"})
    
        response= await call_next(request)
        return response
        