# tests/conftest.py
import pytest 
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
        
@pytest.fixture
async def auth_token(client):
    resp = await client.post(
        "/v1/auth/token",
        data={"username": "dev", "password": "password"},
    )
    return resp.json()["access_token"]
 
@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture(autouse=True)
def reset_rate_limiter():
    from main import limiter
    limiter.reset()
    yield
