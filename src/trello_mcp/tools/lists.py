from typing import Any

from trello_mcp.client import TrelloClient


async def get_board_lists(board_id: str) -> list[dict[str, Any]]:
    """Return all lists on a board."""
    client = TrelloClient()
    lists = await client.get(
        f"/boards/{board_id}/lists",
        params={"fields": "name,closed,pos"},
    )
    return [
        {
            "id": lst["id"],
            "name": lst["name"],
            "closed": lst["closed"],
            "position": lst["pos"],
        }
        for lst in lists
    ]


async def create_list(board_id: str, name: str, position: str = "bottom") -> dict[str, Any]:
    """Create a new list on a board."""
    client = TrelloClient()
    lst = await client.post(
        "/lists",
        params={"name": name, "idBoard": board_id, "pos": position},
    )
    return {
        "id": lst["id"],
        "name": lst["name"],
        "closed": lst["closed"],
        "position": lst["pos"],
    }
