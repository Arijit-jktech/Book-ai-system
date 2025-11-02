import pytest
from httpx import AsyncClient
from app.main import app
from app.db.init_db import init_db
import asyncio

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope="module", autouse=True)
async def prepare_db():
    await init_db()
    yield

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
