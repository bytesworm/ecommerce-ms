import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 1 minute
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
async def init(db_engine: AsyncEngine) -> None:
    logger.info("🔄 Trying connect to the database..")
    try:
        async with AsyncSession(db_engine) as session:
            await session.execute(text("SELECT 1"))
        logger.info("✅ Successfully connected to database")
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        raise


async def main() -> None:
    logger.info("Initializing service")
    await init(engine)
    logger.info("Service initialized")


if __name__ == "__main__":
    asyncio.run(main())
