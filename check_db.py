import asyncio, asyncpg, os

async def main():
    conn = await asyncpg.connect(
        f"postgresql://admin4000:{os.getenv('postgres_pwd')}@uptimemonitor-db.postgres.database.azure.com:5432/postgres",
        ssl="require"
    )
    rows = await conn.fetch("SELECT * FROM check_results ORDER BY checked_at DESC LIMIT 5")
    for r in rows:
        print(dict(r))
    if not rows:
        print("No results yet")
    await conn.close()

asyncio.run(main())
