# tests/integration/test_module1.py
from unittest.mock import AsyncMock
from agents.graph import agent_graph

# GET /health returns 200 with version field
async def test_health_return_200(client):
    r = await client.get('/health')
    assert r.status_code == 200
    assert 'version' in r.json()

# GET /ready returns 200
async def test_ready_return_200(client):
    r = await client.get('/ready')
    assert r.status_code == 200

# POST /v1/auth/token returns JWT on valid credentials
async def test_auth_token_issued_on_valid_credentials(client):
    r = await client.post(
        "/v1/auth/token",
        data={"username":"dev", "password":"password"},
    )
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    
# POST /v1/auth/token returns 400 on invalid credentials
async def test_auth_token_rejected_on_bad_credentials(client):
    r = await client.post(
        "/v1/auth/token",
        data={"username":"dev", "password":"wrong-password"},
    )
    assert r.status_code == 400

# POST /v1/agents/chat returns 401 without a token
async def test_chat_endpoint_requires_auth(client):
    r = await client.post(
        "/v1/agents/chat?prompt=hello"
    )
    assert r.status_code == 401
    
# POST /v1/agents/chat streams tokens back with a valid token
async def _fake_invoke(state):
    return {**state, "final_output": "stub response"}

async def test_chat_endpoint_streams_response(client, auth_headers, monkeypatch):
    monkeypatch.setattr(agent_graph, "ainvoke", AsyncMock(side_effect=_fake_invoke))
    async with client.stream(
        "POST", "/v1/agents/chat?prompt=hello", headers=auth_headers
    ) as r:
        assert r.status_code == 200
        chunks = [c async for c in r.aiter_text()]
    body = "".join(chunks)
    assert "data:" in body
    assert "[DONE]" in body
    # Split on SSE event boundaries to verify multiple messages were streamed
    events = [e for e in body.split("\n\n") if e.strip()]
    assert len(events) > 1 
    
# Rate limiter returns 429 after 20 requests/minute
async def test_rate_limit_triggers_after_threshold(client, auth_headers, monkeypatch):
    monkeypatch.setattr(agent_graph, "ainvoke", AsyncMock(side_effect=_fake_invoke))
    statuses = []
    for _ in range(21):
        r = await client.post("/v1/agents/chat?prompt=hi", headers=auth_headers)
        statuses.append(r.status_code)
    assert 429 in statuses



# {
#     "status": "ready",
# }
# 200 OK

# {
#     "status": "ok",
#     "version": "1.0.0"
# }
# 	200 OK

# {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYiLCJleHAiOjE3ODYwMzc0ODZ9.13BkZ2NCWnQCsXpP4K6RXhpQiXUxdSjZKHvWkUIANB0",
#     "token_type": "bearer"
# }
# 200 OK

# {
#     "detail": "Incorrect credentials"
# }
# 400 BAD REQUEST

# {
#     "detail": "Not authenticated"
# }
# 401 UNAUTHORIZED

# data: Echo:
# data: hello
# data: [DONE]
# 200 OK

# {
#     "error": "Rate limit exceeded: 20 per 1 minute"
# }
# 429 TOO MANY REQUESTS
