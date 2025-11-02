from typing import List
from app.models.book import Book

async def recommend_books_by_genre(books: List[Book], preferred_genre: str, limit: int = 5):
    matches = [b for b in books if b.genre and preferred_genre.lower() in b.genre.lower()]
    matches.sort(key=lambda b: b.year_published or 0, reverse=True)
    return matches[:limit]
