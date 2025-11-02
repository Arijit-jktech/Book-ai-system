from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=False)
    genre = Column(String(100), nullable=True, index=True)
    year_published = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
