#connection pooling
import asyncpg
import os
import redis
pool: asyncpg.Pool | None = None

def get_redis():
    host= os.environ.get("REDIS_HOST", "localhost")
    port = int(os.environ.get("REDIS_PORT", 6379))
    password = os.environ.get("REDIS_PASSWORD", None)
    use_ssl = os.environ.get("REDIS_SSL", "false").lower() == "true"
    return redis.Redis(host=host, port=port, password=password, ssl=use_ssl, decode_responses=True)


async def init_pool():
    global pool
    pwd= os.getenv("postgres_pwd")
    pool = await asyncpg.create_pool(
        dsn=f"postgresql://admin4000:{pwd}@uptimemonitor-db.postgres.database.azure.com/postgres",
        min_size=5,     # always keep 5 connections warm
        max_size=20,    # never exceed 20 connections
        ssl="require"
    )

async def close_pool():
    await pool.close()

async def get_db():
    conn= await pool.acquire()
    try:
        yield conn
    finally:
        await pool.release(conn)
