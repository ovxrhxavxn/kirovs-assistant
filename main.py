import asyncio

from src.presentation.bot.main import start as start_bot
from src.database.sqlalchemy.config import create_tables


async def main():
    await create_tables()
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())