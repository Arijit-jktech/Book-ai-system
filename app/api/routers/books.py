from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_role
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.schemas.review import ReviewOut, ReviewCreate
from app.db.session import get_session
from app.crud import books as crud_books
from app.crud import reviews as crud_reviews
from app.services.llama import generate_summary_from_text
from app.services.recommendations import recommend_books_by_genre

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookOut, dependencies=[Depends(require_role("admin"))])
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_session)):
    return await crud_books.create_book(db, book_in)

@router.get("/", response_model=List[BookOut])
async def list_books(db: AsyncSession = Depends(get_session)):
    return await crud_books.get_books(db)

@router.get("/{book_id}", response_model=BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(get_session)):
    obj = await crud_books.get_book(db, book_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Book not found")
    return obj

@router.put("/{book_id}", response_model=BookOut, dependencies=[Depends(require_role("admin"))])
async def update_book(book_id: int, book_in: BookUpdate, db: AsyncSession = Depends(get_session)):
    obj = await crud_books.update_book(db, book_id, book_in)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj

@router.delete("/{book_id}", dependencies=[Depends(require_role("admin"))])
async def delete_book(book_id: int, db: AsyncSession = Depends(get_session)):
    ok = await crud_books.delete_book(db, book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"ok": True}

@router.post("/{book_id}/reviews", response_model=ReviewOut)
async def add_review(book_id: int, review_in: ReviewCreate, db: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    b = await crud_books.get_book(db, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    return await crud_reviews.create_review(db, book_id, review_in)

@router.get("/{book_id}/reviews", response_model=List[ReviewOut])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_session)):
    return await crud_reviews.get_reviews_for_book(db, book_id)

@router.get("/{book_id}/summary")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_session)):
    b = await crud_books.get_book(db, book_id)
    if not b:
        raise HTTPException(status_code=404, detail="Book not found")
    summary = b.summary
    if not summary:
        seed = f"{b.title} by {b.author} - genre {b.genre or ''}"
        summary = await generate_summary_from_text(seed)
        from app.schemas.book import BookUpdate
        await crud_books.update_book(db, book_id, BookUpdate(summary=summary))
    avg_rating = await crud_reviews.get_average_rating(db, book_id)
    return {"id": b.id, "title": b.title, "summary": summary, "avg_rating": avg_rating}

@router.get("/recommendations")
async def recommendations(pref_genre: str = "fiction", limit: int = 5, db: AsyncSession = Depends(get_session)):
    all_books = await crud_books.get_books(db)
    recs = await recommend_books_by_genre(all_books, pref_genre, limit)
    return [ {"id": b.id, "title": b.title, "genre": b.genre} for b in recs ]
