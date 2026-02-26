from typing import Any

from trello_mcp.client import TrelloClient


async def get_board_labels(board_id: str) -> list[dict[str, Any]]:
    """Return all labels on a board."""
    client = TrelloClient()
    labels = await client.get(f"/boards/{board_id}/labels")
    return [
        {
            "id": lb["id"],
            "name": lb.get("name", ""),
            "color": lb.get("color", ""),
        }
        for lb in labels
    ]


async def create_label(
    board_id: str, name: str, color: str = "blue"
) -> dict[str, Any]:
    """Create a label on a board.

    Valid colors: yellow, purple, blue, red, green, orange, black, sky, pink, lime.
    """
    client = TrelloClient()
    lb = await client.post(
        "/labels",
        params={"name": name, "color": color, "idBoard": board_id},
    )
    return {
        "id": lb["id"],
        "name": lb.get("name", ""),
        "color": lb.get("color", ""),
    }
