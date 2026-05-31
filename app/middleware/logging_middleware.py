from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid
import time
import logging  
import json
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        ip=request.client.host
        startTime= time.time()
        request_id= str(uuid.uuid4())
        response= await call_next(request)
        endTime=time.time()
        latency_ms= (endTime-startTime)*1000
        status= response.status_code
        method=request.method
        path= request.url.path
        logging.info(json.dumps({"timestamp":startTime, "level": "INFO", "method":method, "path":path, "status":status, "latency_ms":latency_ms, "ip":ip, "request_id":request_id}))
        return response
        