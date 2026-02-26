from typing import Any

from trello_mcp.client import TrelloClient


async def list_my_boards() -> list[dict[str, Any]]:
    """Return all boards for the authenticated user."""
    client = TrelloClient()
    boards = await client.get("/members/me/boards", params={"fields": "name,desc,url,closed"})
    return [
        {
            "id": b["id"],
            "name": b["name"],
            "description": b.get("desc", ""),
            "url": b["url"],
            "closed": b["closed"],
        }
        for b in boards
    ]


async def get_board(board_id: str) -> dict[str, Any]:
    """Return details of a single board."""
    client = TrelloClient()
    b = await client.get(
        f"/boards/{board_id}",
        params={"fields": "name,desc,url,closed,prefs,dateLastActivity"},
    )
    return {
        "id": b["id"],
        "name": b["name"],
        "description": b.get("desc", ""),
        "url": b["url"],
        "closed": b["closed"],
        "date_last_activity": b.get("dateLastActivity"),
    }
