from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate

async def create_book(db: AsyncSession, book_in: BookCreate) -> Book:
    obj = Book(**book_in.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_book(db: AsyncSession, book_id: int) -> Optional[Book]:
    q = await db.get(Book, book_id)
    return q

async def get_books(db: AsyncSession, limit: int = 100) -> List[Book]:
    result = await db.execute(select(Book).limit(limit))
    return result.scalars().all()

async def update_book(db: AsyncSession, book_id: int, book_in: BookUpdate) -> Optional[Book]:
    obj = await db.get(Book, book_id)
    if not obj:
        return None
    for k, v in book_in.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_book(db: AsyncSession, book_id: int) -> bool:
    obj = await db.get(Book, book_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True
