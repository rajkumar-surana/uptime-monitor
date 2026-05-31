from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_pool , close_pool
from app.routes import health, auth, monitor
from app.workers.checker import run_checker
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimitMiddleware
import uvicorn
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pool()
    task= asyncio.create_task(run_checker())
    yield
    task.cancel()
    await close_pool()

app= FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(monitor.router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)