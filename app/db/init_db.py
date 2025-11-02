from app.db.session import engine
from app.db.base import Base
from app.models.book import Book
from app.models.review import Review

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
