import uvicorn
from app.api.api import create_app
from app.core.config import settings
from app.db.init_db import init_db

app = create_app()

@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
