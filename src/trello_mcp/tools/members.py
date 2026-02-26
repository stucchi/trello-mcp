from typing import Any

from trello_mcp.client import TrelloClient


async def get_me() -> dict[str, Any]:
    """Return the authenticated Trello member."""
    client = TrelloClient()
    m = await client.get("/members/me")
    return {
        "id": m["id"],
        "username": m.get("username", ""),
        "full_name": m.get("fullName", ""),
        "url": m.get("url", ""),
    }
