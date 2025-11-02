from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.models.review import Review
from app.schemas.review import ReviewCreate

async def create_review(db: AsyncSession, book_id: int, review_in: ReviewCreate) -> Review:
    obj = Review(book_id=book_id, **review_in.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_reviews_for_book(db: AsyncSession, book_id: int) -> List[Review]:
    result = await db.execute(select(Review).where(Review.book_id == book_id))
    return result.scalars().all()

async def get_average_rating(db: AsyncSession, book_id: int):
    result = await db.execute(select(Review.rating).where(Review.book_id == book_id))
    ratings = [r[0] for r in result.all()]
    if not ratings:
        return None
    return sum(ratings)/len(ratings)
