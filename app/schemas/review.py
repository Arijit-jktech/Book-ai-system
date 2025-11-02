from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    user_id: str
    review_text: str
    rating: float

class ReviewOut(ReviewCreate):
    id: int
    book_id: int
    class Config:
        orm_mode = True
