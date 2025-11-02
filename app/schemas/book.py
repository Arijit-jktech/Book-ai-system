from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None
    summary: Optional[str] = None

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    year_published: Optional[int]
    summary: Optional[str]

class BookOut(BookCreate):
    id: int
    class Config:
        orm_mode = True
