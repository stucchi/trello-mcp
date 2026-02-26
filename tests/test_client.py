import pytest

from trello_mcp.client import TrelloClient
from trello_mcp.exceptions import (
    TrelloAuthError,
    TrelloError,
    TrelloNotFoundError,
    TrelloRateLimitError,
)


@pytest.mark.asyncio
async def test_get_success(httpx_mock):
    httpx_mock.add_response(json={"id": "abc123", "name": "Test"})
    client = TrelloClient()
    result = await client.get("/boards/abc123")
    assert result == {"id": "abc123", "name": "Test"}


@pytest.mark.asyncio
async def test_get_auth_params_sent(httpx_mock):
    httpx_mock.add_response(json={})
    client = TrelloClient()
    await client.get("/members/me")
    request = httpx_mock.get_request()
    assert "key=test-key" in str(request.url)
    assert "token=test-token" in str(request.url)


@pytest.mark.asyncio
async def test_get_401(httpx_mock):
    httpx_mock.add_response(status_code=401)
    client = TrelloClient()
    with pytest.raises(TrelloAuthError):
        await client.get("/boards/x")


@pytest.mark.asyncio
async def test_get_404(httpx_mock):
    httpx_mock.add_response(status_code=404)
    client = TrelloClient()
    with pytest.raises(TrelloNotFoundError):
        await client.get("/boards/doesnotexist")


@pytest.mark.asyncio
async def test_get_429(httpx_mock):
    httpx_mock.add_response(status_code=429)
    client = TrelloClient()
    with pytest.raises(TrelloRateLimitError):
        await client.get("/boards/x")


@pytest.mark.asyncio
async def test_get_500(httpx_mock):
    httpx_mock.add_response(status_code=500, text="Internal Server Error")
    client = TrelloClient()
    with pytest.raises(TrelloError, match="500"):
        await client.get("/boards/x")


@pytest.mark.asyncio
async def test_post_success(httpx_mock):
    httpx_mock.add_response(json={"id": "new123"})
    client = TrelloClient()
    result = await client.post("/cards", params={"name": "Test Card"})
    assert result["id"] == "new123"


@pytest.mark.asyncio
async def test_put_success(httpx_mock):
    httpx_mock.add_response(json={"id": "card1", "name": "Updated"})
    client = TrelloClient()
    result = await client.put("/cards/card1", params={"name": "Updated"})
    assert result["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_success(httpx_mock):
    httpx_mock.add_response(json={"_value": None})
    client = TrelloClient()
    result = await client.delete("/cards/card1")
    assert result is not None
