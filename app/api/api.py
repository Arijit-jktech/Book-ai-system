from fastapi import FastAPI
from app.api.routers import auth, books, reviews
from app.core.config import settings

def create_app():
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(auth.router, prefix="/api")
    app.include_router(books.router, prefix="/api")
    app.include_router(reviews.router, prefix="/api")
    return app
