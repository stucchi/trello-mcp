from typing import Any

from trello_mcp.client import TrelloClient


async def search_trello(
    query: str,
    model_types: str = "cards,boards",
    board_ids: list[str] | None = None,
    cards_limit: int = 10,
    boards_limit: int = 5,
) -> dict[str, Any]:
    """Search Trello for cards and/or boards matching a query."""
    client = TrelloClient()
    params: dict[str, Any] = {
        "query": query,
        "modelTypes": model_types,
        "cards_limit": cards_limit,
        "boards_limit": boards_limit,
    }
    if board_ids:
        params["idBoards"] = ",".join(board_ids)

    data = await client.get("/search", params=params)

    result: dict[str, Any] = {}
    if "cards" in data:
        result["cards"] = [
            {
                "id": c["id"],
                "name": c["name"],
                "description": c.get("desc", ""),
                "url": c.get("url", ""),
                "closed": c.get("closed", False),
                "list_id": c.get("idList", ""),
                "board_id": c.get("idBoard", ""),
            }
            for c in data["cards"]
        ]
    if "boards" in data:
        result["boards"] = [
            {
                "id": b["id"],
                "name": b["name"],
                "description": b.get("desc", ""),
                "url": b.get("url", ""),
                "closed": b.get("closed", False),
            }
            for b in data["boards"]
        ]
    return result
