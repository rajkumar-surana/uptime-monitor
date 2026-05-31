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
    host = os.getenv("postgres_host", "localhost")
    port = os.getenv("postgres_port", "5432")
    user = os.getenv("postgres_user", "admin4000")
    pwd = os.getenv("postgres_pwd")
    db = os.getenv("postgres_db", "postgres")
    pool = await asyncpg.create_pool(
        dsn=f"postgresql://{user}:{pwd}@{host}:{port}/{db}",
        min_size=5,
        max_size=20,
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
