import pytest

from httpx import AsyncClient

from app import create_app
from fastapi.testclient import TestClient

@pytest.fixture
def app():
    yield create_app("test")

@pytest.fixture
def client(app):
    client = TestClient(app)
    yield  client

@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://") as client:
        yield client
