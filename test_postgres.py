import asyncio

from sqlalchemy import text

from app.db.postgres_database import postgres_engine


async def test_connection():
    try:
        async with postgres_engine.connect() as connection:
            result = await connection.execute(
                text("SELECT current_database()")
            )

            print(result.scalar_one())
    finally:
        await postgres_engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())